from django.contrib import admin
from .models import BookModel, AuthorModel, BookAuthorModel
# Register your models here.

admin.site.register(BookModel)
admin.site.register(AuthorModel)
admin.site.register(BookAuthorModel)