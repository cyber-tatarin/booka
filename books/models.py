from django.db import models
from django_resized import ResizedImageField
from users.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

class BookModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    image = ResizedImageField(size=[500, 500], crop=['middle', 'center'], quality=99,
                              blank=True, null=True, upload_to='images/', default='images/default.jpg')
    name = models.CharField(max_length=100)
    year = models.IntegerField(default=0)
    language = models.CharField(max_length=100)
    description = models.CharField(max_length=600)
    book_type = models.IntegerField(default=1)
    author = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class AuthorModel(models.Model):
    name = models.CharField(max_length=50)
    books = models.ManyToManyField(BookModel, through='BookAuthorModel')
    def __str__(self):
        return self.name

class BookAuthorModel(models.Model):
    book_name = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    author_name = models.ForeignKey(AuthorModel, on_delete=models.CASCADE)

