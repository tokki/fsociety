from django.db import models


# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    year = models.CharField(max_length=10)
    fullname = models.CharField(max_length=100)
    category = models.CharField(max_length=40)
    director = models.CharField(max_length=100)
    writer = models.CharField(max_length=100)
    imdb = models.CharField(max_length=20)
    douban = models.CharField(max_length=20)
    rating = models.CharField(max_length=10)
    actor = models.CharField(max_length=1000)
    cover = models.CharField(max_length=100)
    is_movie = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    url = models.CharField(max_length=100)

    def __str__(self):
        return self.name + '---' + self.imdb


class Seed(models.Model):
    imdb = models.CharField(max_length=20)
    filename = models.CharField(max_length=100)
    size = models.CharField(max_length=20)
    quality = models.CharField(max_length=20)
    magnet = models.CharField(max_length=500)

    def __str__(self):
        return self.filename
