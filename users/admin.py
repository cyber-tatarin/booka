from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Contacts, Cities

User = get_user_model()


@admin.register(User)
class UserAdm(UserAdmin):
    list_display = ('username', 'city')


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('contact', 'description')


admin.site.register(Cities)
