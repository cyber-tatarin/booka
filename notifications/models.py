from django.db import models
from users.models import User
from books.models import BookModel


class Notifications(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=350, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    ntype = models.IntegerField()
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)

    #добавить фк на книгу



