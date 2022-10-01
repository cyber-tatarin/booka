from django.db import models
from users.models import User


class Notifications(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=350, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    ntype = models.IntegerField()

    #добавить фк на книгу



