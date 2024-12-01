from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Room, Meme, Vote
from rest_framework.exceptions import ValidationError

User = get_user_model()

class RoomTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.room_data = {
            'name': 'Test Room',
            'max_capacity': 10
        }
        self.room_url = reverse('room-list')  # Oda listesi URL'si, gerekli şekilde ayarlayın

    def test_create_room(self):
        # Oda oluşturma
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.room_url, self.room_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.room_data['name'])

    def test_room_capacity_validation(self):
        # Geçersiz kapasite ile oda oluşturma
        invalid_room_data = self.room_data.copy()
        invalid_room_data['max_capacity'] = -5
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.room_url, invalid_room_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Max capacity must be greater than 0", str(response.data))

    def test_update_room(self):
        # Oda güncelleme
        room = Room.objects.create(**self.room_data)
        update_url = reverse('room-detail', kwargs={'pk': room.id})
        updated_data = {'name': 'Updated Room', 'max_capacity': 15}
        self.client.login(username='testuser', password='testpass')
        response = self.client.put(update_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])

    def test_update_room_permission(self):
        # Başka bir kullanıcıyla oda güncelleme denemesi
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        room = Room.objects.create(**self.room_data)
        update_url = reverse('room-detail', kwargs={'pk': room.id})
        updated_data = {'name': 'Updated Room', 'max_capacity': 15}
        self.client.login(username='otheruser', password='otherpass')
        response = self.client.put(update_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_room(self):
        # Oda silme
        room = Room.objects.create(**self.room_data)
        delete_url = reverse('room-detail', kwargs={'pk': room.id})
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_room_retrieval(self):
        # Oda bilgilerini görüntüleme
        room = Room.objects.create(**self.room_data)
        retrieve_url = reverse('room-detail', kwargs={'pk': room.id})
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.room_data['name'])


class MemeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.meme_data = {
            'name': 'Test Meme',
            'image_url': 'http://example.com/meme.jpg'
        }

    def test_create_meme(self):
        # Meme oluşturma
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('create-meme'), self.meme_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.meme_data['name'])

    def test_meme_retrieval(self):
        # Meme görüntüleme
        meme = Meme.objects.create(**self.meme_data)
        retrieve_url = reverse('meme-detail', kwargs={'pk': meme.id})
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.meme_data['name'])


class VoteTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.meme = Meme.objects.create(name='Test Meme', image_url='http://example.com/meme.jpg')
        self.vote_data = {
            'meme': self.meme.id,
            'voter': self.user.id
        }
        self.vote_url = reverse('vote-list')  # Oylama listesi URL'si, gerekli şekilde ayarlayın

    def test_create_vote(self):
        # Oy verme
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.vote_url, self.vote_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['meme'], self.meme.id)

    def test_multiple_votes_validation(self):
        # Aynı meme için birden fazla oy verme denemesi
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.vote_url, self.vote_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.vote_url, self.vote_data)  # Aynı oyu bir kez daha gönderiyoruz
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You have already voted for this meme", str(response.data))


class UserTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        # Kullanıcı listesi URL'si, gerekli şekilde ayarlayın

    def test_create_user(self):
        # Kullanıcı oluşturma
        response = self.client.post(reverse("user-register"), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], self.user_data['username'])

    def test_user_retrieval(self):
        # Kullanıcı bilgilerini görüntüleme
        user = User.objects.create_user(username='testuser', password='testpass')
        retrieve_url = reverse('user-detail', kwargs={'pk': user.id})
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')


class PermissionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpass')
        self.room_data = {
            'name': 'Test Room',
            'max_capacity': 10
        }

    def test_room_update_permission(self):
        # Oda güncelleme izni
        room = Room.objects.create(**self.room_data)
        update_url = reverse('room-update', kwargs={'pk': room.id})
        updated_data = {'name': 'Updated Room', 'max_capacity': 15}
        
        # Diğer kullanıcıyla oda güncellenmeye çalışılması
        self.client.login(username='otheruser', password='otherpass')
        response = self.client.put(update_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_room_access_permission(self):
        # Oda bilgilerini erişim izni
        room = Room.objects.create(**self.room_data)
        retrieve_url = reverse('room-detail', kwargs={'pk': room.id})
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Diğer kullanıcıyla odanın bilgilerine erişim
        self.client.login(username='otheruser', password='otherpass')
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
