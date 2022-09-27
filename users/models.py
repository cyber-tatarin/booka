from django.contrib.auth.models import AbstractUser
from django.db import models
from django_resized import ResizedImageField


class Cities(models.Model):
    city = models.CharField(max_length=200, null=True, blank=True)


class User(AbstractUser):
    email = models.EmailField(null=True, blank=False, unique=True)
    photo = ResizedImageField(size=[500, 500], crop=['middle', 'center'], quality=99,
                              blank=True, null=True, upload_to='images')
    bio = models.CharField(max_length=200, null=True, blank=True)
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True)


class Contacts(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_type = models.CharField(max_length=25, null=True, blank=True, unique=True)
    contact = models.CharField(max_length=50, null=True, blank=True, unique=True)

