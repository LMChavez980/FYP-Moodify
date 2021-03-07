from django.db import models
from django.contrib.postgres.fields import ArrayField


class User(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)


class ClassifiedSong(models.Model):
    song_id = models.CharField(max_length=22, primary_key=True)
    song_name = models.TextField(null=False)
    artists = models.TextField(null=False)


class MoodPlaylist(models.Model):
    playlist_id = models.CharField(max_length=22, primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)






