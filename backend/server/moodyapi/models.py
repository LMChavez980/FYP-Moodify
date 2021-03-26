from django.db import models
from django.contrib.postgres.fields import ArrayField


class User(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    user_songs = ArrayField(models.CharField(max_length=22))


class ClassifiedSong(models.Model):
    moods = [("happy", "happy"), ("sad", "sad"), ("relaxed", "relaxed"), ("angry", "angry")]
    song_id = models.CharField(max_length=22, primary_key=True)
    song_name = models.TextField(null=False)
    artists = models.TextField(null=False)
    mood = models.CharField(max_length=8, choices=moods, default="")


class MoodPlaylist(models.Model):
    moods = [("happy", "happy"), ("sad", "sad"), ("relaxed", "relaxed"), ("angry", "angry")]
    playlist_id = models.CharField(max_length=22, primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=8, choices=moods, default="")






