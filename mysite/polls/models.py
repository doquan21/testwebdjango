from django.db import models


# Create your models here.

class Song(models.Model):
    song_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    singer = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    song = models.FileField(upload_to='images')

    def __str__(self):
        return self.name +' id:'+ str(self.song_id)

class playlist_user(models.Model):
    username = models.CharField(max_length=200)

    def __str__(self):
        return f'Username = {self.username}, Liked Songs = {list(self.playlist_song_set.all())}'





