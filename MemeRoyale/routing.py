from django.urls import re_path
from consumers import RoomConsumer, MemeConsumer, VoteConsumer, TimerConsumer


websocket_urlpatterns = [
    re_path(r'ws/room/(?P<room_name>\w+)/$', RoomConsumer.as_asgi()),
    re_path(r'ws/room/(?P<room_name>\w+)/meme/$', MemeConsumer.as_asgi()),
    re_path(r'ws/room/(?P<room_name>\w+)/vote/$', VoteConsumer.as_asgi()),
    re_path(r'ws/room/(?P<room_name>\w+)/timer/$', TimerConsumer.as_asgi()),
]
