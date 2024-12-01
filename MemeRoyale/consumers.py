import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from asgiref.sync import sync_to_async
import redis
from datetime import datetime


def get_room_group_name(scope, prefix='room'):
    """
    Verilen scope ve prefix ile grup adı oluşturur.
    """
    room_name = scope['url_route']['kwargs']['room_name']
    return f"{prefix}_{room_name}"


class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = get_room_group_name(self.scope)

        # Odaya katıl
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Kullanıcı kimlik doğrulama kontrolü
        if not self.scope['user'].is_authenticated:
            await self.send(text_data=json.dumps({'error': 'Authentication required'}))
            return

        # Kullanıcı katılım bilgisi yayınla
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_join',
                'username': self.scope['user'].username if self.scope['user'].is_authenticated else "Anonymous"
            }
        )

    async def disconnect(self, close_code):
        # Odadan ayrıl
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Kullanıcı ayrılma bilgisini yayınla
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_leave',
                'username': self.scope['user'].username if self.scope['user'].is_authenticated else "Anonymous"
            }
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get('message', None)

            if message:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'username': self.scope['user'].username if self.scope['user'].is_authenticated else "Anonymous",
                        'timestamp': datetime.now().isoformat()
                    }
                )
        except Exception as e:
            await self.send(text_data=json.dumps({'error': str(e)}))

    async def user_join(self, event):
        # Kullanıcı katılım bilgisini frontend'e gönder
        await self.send(text_data=json.dumps({
            'type': 'user_join',
            'username': event['username']
        }))

    async def user_leave(self, event):
        # Kullanıcı ayrılma bilgisini frontend'e gönder
        await self.send(text_data=json.dumps({
            'type': 'user_leave',
            'username': event['username']
        }))


class TimerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = get_room_group_name(self.scope, prefix='timer')

        # Odaya katıl
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Odadan ayrıl
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            seconds = data.get('seconds')

            # Zamanlayıcı başlat
            if seconds is None or seconds <= 0:
                await self.send(text_data=json.dumps({'error': 'Invalid timer value'}))
                return

            await self.start_timer(seconds)
        except Exception as e:
            await self.send(text_data=json.dumps({'error': str(e)}))

    async def start_timer(self, seconds):
        redis_instance = redis.Redis()
        key = f"timer:{self.room_group_name}"

        await sync_to_async(redis_instance.set)(key, seconds)

        while seconds > 0:
            await asyncio.sleep(1)
            seconds -= 1
            await sync_to_async(redis_instance.set)(key, seconds)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'timer_update',
                    'time_left': seconds
                }
            )

        # Zamanlayıcı bittiğinde Redis'ten temizleme
        await sync_to_async(redis_instance.delete)(key)

    async def timer_update(self, event):
        time_left = event['time_left']

        # Zamanlayıcı bilgisini frontend'e gönder
        await self.send(text_data=json.dumps({
            'action': 'timer',
            'time_left': time_left
        }))


class VoteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = get_room_group_name(self.scope, prefix='vote')

        # Odaya katıl
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Odadan ayrıl
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            vote = data.get('vote')

            if vote is None:
                await self.send(text_data=json.dumps({'error': 'Invalid vote value'}))
                return

            # Oylama bilgisini gruba gönder
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'vote_update',
                    'vote': vote
                }
            )
        except Exception as e:
            await self.send(text_data=json.dumps({'error': str(e)}))

    async def vote_update(self, event):
        vote = event['vote']

        # Oylama bilgisini frontend'e gönder
        await self.send(text_data=json.dumps({
            'action': 'vote',
            'vote': vote
        }))


class MemeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = get_room_group_name(self.scope, prefix='meme')

        # Odaya katıl
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Odadan ayrıl
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            meme_update = data.get('meme_update')

            if meme_update is None:
                await self.send(text_data=json.dumps({'error': 'Invalid meme update'}))
                return

            # Meme güncellemesini gruba gönder
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'meme_update',
                    'meme_update': meme_update
                }
            )
        except Exception as e:
            await self.send(text_data=json.dumps({'error': str(e)}))

    async def meme_update(self, event):
        meme_update = event['meme_update']

        # Meme güncellemesini frontend'e gönder
        await self.send(text_data=json.dumps({
            'action': 'update_meme',
            'meme_update': meme_update
        }))
