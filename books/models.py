from django.db import models
from django_resized import ResizedImageField
from users.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


class AuthorModel(models.Model):
    name = models.CharField(max_length=60)


class BookModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = ResizedImageField(size=[500, 500], crop=['middle', 'center'], quality=99,
                              blank=True, null=True, upload_to='images/')
    name = models.CharField(max_length=100)
    year = models.IntegerField(null=True)
    language = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=600, null=True)
    book_type = models.IntegerField(default=1)
    authors = models.ManyToManyField(AuthorModel, related_name='authrs')

    def __str__(self):
        return self.name



