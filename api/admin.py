from django.contrib import admin
from .models import User, Room, Round, Meme, Vote

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Round)
admin.site.register(Meme)
admin.site.register(Vote)
