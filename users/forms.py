from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
import re
from django.core.validators import EmailValidator

User = get_user_model()


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(max_length=254,
                             error_messages={'required': 'lola.',
                                             'invalid': 'raaaa'},
                             widget=forms.EmailInput({
                                 'required': True,
                                 'class': 'form-control',
                                 'placeholder': 'E-mail address',
                             }))

    username = forms.CharField(max_length=100, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'id': "username",
                                                             'aria-describedby': "username-help"}))

    password1 = forms.CharField(max_length=100, required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'id': "username",
                                                                  'aria-describedby': "username-help"}))

    password2 = forms.CharField(max_length=100, required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'id': "username",
                                                                  'aria-describedby': "username-help"}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']

        if re.search(r'[^a-z_1234567890]', username):
            raise forms.ValidationError("Никнейм может состоять только из латинских букв нижнего регистра, цифр и _ ")
        return username


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'Неправильный логин или пароль'
        super().__init__(*args, **kwargs)

    username = forms.CharField(max_length=100, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'id': "username",
                                                             'aria-describedby': "username-help"}))

    password = forms.CharField(max_length=100, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'id': "username",
                                                                 'aria-describedby': "username-help"}))
