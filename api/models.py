from django.utils.timezone import now, timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    games_won = models.PositiveIntegerField(default=0)
    games_played = models.PositiveIntegerField(default=0)

    @property
    def win_rate(self):
        if self.games_played == 0:
            return 0
        return round((self.games_won / self.games_played) * 100, 2)

    def __str__(self):
        return self.username


class Room(models.Model):
    ROOM_STATUS_CHOICES = (
        ('waiting', 'Waiting'),
        ('active', 'Active'),
        ('ended', 'Ended')
    )

    THEME_CHOICES = (
        ('memes', 'Memes'),
        ('animals', 'Animals'),
        ('movies', 'Movies'),
        ('sports', 'Sports'),
        ('music', 'Music'),
        ('technology', 'Technology'),
        ('food', 'Food'),
        ('nature', 'Nature'),
        ('gaming', 'Gaming'),
        ('art', 'Art'),
    )
    
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_rooms')
    participants = models.ManyToManyField(User, related_name='rooms', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    meme_count = models.PositiveIntegerField(default=0)
    max_capacity = models.PositiveIntegerField(default=4)
    theme = models.CharField(max_length=100, choices=THEME_CHOICES, blank=True)
    status = models.CharField(max_length=20, choices=ROOM_STATUS_CHOICES, default='waiting')
    duration = models.PositiveIntegerField(default=300)
    
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def is_full(self):
        return self.participants.count() >= self.max_capacity

    def add_participant(self, user):
        if not self.is_full():
            self.participants.add(user)
            return True
        return False

    def remove_participant(self, user):
        self.participants.remove(user)
        return True

    def start_game(self):
        self.start_time = timezone.now()
        self.save()

    def end_game(self):
        self.end_time = timezone.now()
        self.save()

    def close_room(self):
        self.status = 'ended'
        self.save()

    def __str__(self):
        return f"Room {self.id} hosted by {self.host.username}"


class Round(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='rounds')
    theme = models.CharField(max_length=255)
    random_image = models.ImageField(upload_to='random_images/', null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_rounds')
    created_at = models.DateTimeField(auto_now_add=True)
    meme_submission_end_time = models.DateTimeField()
    voting_start_time = models.DateTimeField(null=True, blank=True)
    voting_end_time = models.DateTimeField(null=True, blank=True)
    voting_ended = models.BooleanField(default=False)

    @property
    def time_remaining(self):
        end_time = self.created_at + timedelta(seconds=self.room.duration)
        return max((end_time - now()).total_seconds(), 0)

    def start_voting(self):
        self.voting_start_time = now()
        self.voting_end_time = self.voting_start_time + timedelta(seconds=60)
        self.save()

    def end_voting(self):
        self.voting_ended = True
        self.save()

        memes = self.memes.all()
        sorted_memes = sorted(memes, key=lambda x: x.total_votes, reverse=True)
        
        winners = sorted_memes[:3]
        
        for i, meme in enumerate(winners):
            meme.creator.games_won += 1
            meme.creator.save()

        self.winner = winners[0].creator
        self.save()

    def __str__(self):
        return f"Round in {self.room.name} - Theme: {self.theme}"


class Meme(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='memes')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memes')
    image = models.ImageField(upload_to='meme_images/')
    caption = models.TextField(blank=True)
    votes = models.ManyToManyField(User, related_name='voted_memes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_votes(self):
        return self.votes.count()

    def __str__(self):
        return f"Meme by {self.creator.username} - Votes: {self.total_votes}"


class Vote(models.Model):
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE, related_name='votes_received')
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes_cast')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('meme', 'voter')

    def __str__(self):
        return f"Vote by {self.voter.username} for {self.meme.creator.username}'s meme"
