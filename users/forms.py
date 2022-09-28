from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
import re

User = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'username']

    def clean_username(self):
        username = self.cleaned_data['username']

        if re.search(r'[^a-z_1234567890]', username):
            raise forms.ValidationError("Никнейм может состоять только из латинских букв нижнего регистра, цифр и _ ")

        return username
