from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import UserSerializer, RoomSerializer, RoundSerializer, MemeSerializer, VoteSerializer
from .models import User, Room, Round, Meme, Vote

class HomePageView(APIView):
    """
    Ana sayfa için genel bilgileri döndüren view.
    """
    permission_classes = [AllowAny]  # Ana sayfa herkesin erişebileceği bir sayfa olacak

    def get(self, request):
        # Son oluşturulan odalar
        latest_rooms = Room.objects.filter(Q(status='active') | Q(status='waiting')).order_by('-created_at')[:5]
        latest_rooms_serializer = RoomSerializer(latest_rooms, many=True)

        # Son kullanıcılar
        latest_users = User.objects.all().order_by('-date_joined')[:5]
        latest_users_serializer = UserSerializer(latest_users, many=True)

        # Ana sayfa bilgilerini döndürme
        data = {
            'latest_rooms': latest_rooms_serializer.data,
            'latest_users': latest_users_serializer.data,
            'message': 'Welcome to the game platform!'
        }

        return Response(data)


# Kullanıcı kaydı için view
class UserCreateView(generics.CreateAPIView):
    """
    Kullanıcı kaydı işlemi.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Herkesin kullanıcı oluşturmasına izin verir

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])  # Şifreyi hashle
        user.save()


class UserLoginView(APIView):
    """
    Kullanıcı giriş işlemi
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        # Kullanıcıyı doğrula
        user = authenticate(username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            return Response({
                'refresh': str(refresh),
                'access': str(access_token),
            }, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Geçersiz giriş bilgileri.'}, status=status.HTTP_401_UNAUTHORIZED)


# Kullanıcı bilgilerini görüntüleme (Read)
class UserDetailView(generics.RetrieveAPIView):
    """
    Kullanıcıyı görüntüleme işlemi.
    Kullanıcı sadece kendi bilgilerini görebilir.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Sadece oturum açmış kullanıcılar erişebilir

    def get_object(self):
        # Bu kısımda yalnızca oturum açmış kullanıcıyı döndürmek için override edebiliriz
        return self.request.user


# Kullanıcı bilgilerini güncelleme
class UserUpdateView(generics.UpdateAPIView):
    """
    Kullanıcı bilgilerini güncelleme işlemi.
    Kullanıcı sadece kendi bilgilerini güncelleyebilir.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Sadece oturum açmış kullanıcılar erişebilir

    def get_object(self):
        # Bu kısımda yalnızca oturum açmış kullanıcıyı döndürmek için override edebiliriz
        return self.request.user


# Oda oluşturma işlemi
class CreateRoomView(generics.CreateAPIView):
    """
    Oda oluşturma işlemi.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]  # Yalnızca oturum açmış kullanıcılar odalar oluşturabilir

    def post(self, request, *args, **kwargs):
        name = request.data.get("name")
        access_token = AccessToken.for_user(request.user)
        if name:
            room = Room.objects.create(name=name, host=request.user)  # Odayı oluşturuyoruz
            response_data = {
                "room": RoomSerializer(room).data,
                "access": str(access_token),  # Token'ı string olarak döndürüyoruz
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({"detail": "Oda adı gereklidir."}, status=status.HTTP_400_BAD_REQUEST)



class JoinRoomView(APIView):
    permission_classes = [IsAuthenticated]  # Yalnızca giriş yapmış kullanıcılar katılabilir

    def get(self, request, room_id):
        try:
            # Odayı veritabanında ara
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Kullanıcıyı odaya ekle
        room.participants.add(request.user)
        room.save()

        # Odaya katılan kullanıcıya başarılı yanıt
        return Response({
            "message": f"Successfully joined room: {room.name}",
            "room_name": room.name,
            "participants": [user.username for user in room.participants.all()]
        }, status=status.HTTP_200_OK)


# Oda bilgilerini görüntüleme
class RoomDetailView(generics.RetrieveAPIView):
    """
    Oda bilgilerini görüntüleme işlemi.
    """
    queryset = Room.objects.all().select_related('host').prefetch_related('participants')
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]  # Yalnızca oturum açmış kullanıcılar odaları görüntüleyebilir


# Oda bilgilerini güncelleme
class RoomUpdateView(generics.UpdateAPIView):
    """
    Oda bilgilerini güncelleme işlemi.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]  # Yalnızca oturum açmış kullanıcılar odaları güncelleyebilir

    def get_object(self):
        room = super().get_object()
        if room.host != self.request.user:
            raise PermissionDenied("Sadece oda sahibi odasını güncelleyebilir.")
        return room


# Oda kapatma işlemi
class CloseRoomView(generics.UpdateAPIView):
    """
    Odayı kapatma işlemi (oyunun sonlanması).
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        room = super().get_object()
        if room.host != self.request.user:
            raise PermissionDenied("Sadece oda sahibi odasını kapatabilir.")
        return room

    def update(self, request, *args, **kwargs):
        room = self.get_object()
        room.close_room()  # Odayı kapatma fonksiyonu
        return super().update(request, *args, **kwargs)


# Round oluşturma
class RoundCreateView(generics.CreateAPIView):
    """
    Yeni bir round başlatma işlemi.
    """
    queryset = Round.objects.all()
    serializer_class = RoundSerializer
    permission_classes = [IsAuthenticated]


# Round bilgilerini görüntüleme
class RoundDetailView(generics.RetrieveAPIView):
    """
    Round bilgilerini görüntüleme işlemi.
    """
    queryset = Round.objects.all()
    serializer_class = RoundSerializer
    permission_classes = [IsAuthenticated]


# Meme gönderme işlemi
class MemeCreateView(generics.CreateAPIView):
    """
    Meme oluşturma işlemi.
    """
    queryset = Meme.objects.all()
    serializer_class = MemeSerializer
    permission_classes = [IsAuthenticated]


# Meme bilgilerini görüntüleme
class MemeDetailView(generics.RetrieveAPIView):
    """
    Meme bilgilerini görüntüleme işlemi.
    """
    queryset = Meme.objects.all()
    serializer_class = MemeSerializer
    permission_classes = [IsAuthenticated]


# Oy verme işlemi
class VoteCreateView(generics.CreateAPIView):
    """
    Meme'ye oy verme işlemi.
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]


# Oylama sonuçlarını görüntüleme
class VoteDetailView(generics.RetrieveAPIView):
    """
    Oylama bilgilerini görüntüleme işlemi.
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]
