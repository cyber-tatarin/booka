from django.contrib.auth.models import AbstractUser
from django.db import models
from django_resized import ResizedImageField


class User(AbstractUser):
    email = models.EmailField(null=True, blank=False, unique=True)
    photo = ResizedImageField(size=[500, 500], crop=['middle', 'center'], quality=99,
                              blank=True, null=True, upload_to='images')
    bio = models.CharField(max_length=200, null=True, blank=True)

