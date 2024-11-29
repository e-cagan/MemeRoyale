from django.urls import path
from .views import HomePageView ,UserCreateView, UserDetailView, UserUpdateView, CreateRoomView, RoomDetailView, RoomUpdateView, CloseRoomView, RoundCreateView, RoundDetailView, MemeCreateView, MemeDetailView, VoteCreateView, VoteDetailView

urlpatterns = [
    # Home sayfası
    path('', HomePageView.as_view(), name='home'),

    # Kullanıcı işlemleri
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('profile/', UserDetailView.as_view(), name='user-profile'),
    path('profile/update/', UserUpdateView.as_view(), name='user-update'),

    # Oda işlemleri
    path('rooms/create/', CreateRoomView.as_view(), name='create-room'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('rooms/<int:pk>/update/', RoomUpdateView.as_view(), name='room-update'),
    path('rooms/<int:pk>/close/', CloseRoomView.as_view(), name='room-close'),

    # Round işlemleri
    path('rounds/create/', RoundCreateView.as_view(), name='create-round'),
    path('rounds/<int:pk>/', RoundDetailView.as_view(), name='round-detail'),

    # Meme işlemleri
    path('memes/create/', MemeCreateView.as_view(), name='create-meme'),
    path('memes/<int:pk>/', MemeDetailView.as_view(), name='meme-detail'),

    # Oy verme işlemleri
    path('votes/create/', VoteCreateView.as_view(), name='create-vote'),
    path('votes/<int:pk>/', VoteDetailView.as_view(), name='vote-detail'),
]
