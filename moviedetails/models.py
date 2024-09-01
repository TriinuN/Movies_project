from django.db import models
from django.contrib.auth.models import User


class SavedMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    movie_title = models.CharField(max_length=255)
    movie_poster = models.CharField(max_length=255)

    def __str__(self):
        return self.movie_title
