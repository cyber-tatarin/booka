from django.forms import ModelForm
from django import forms
import re
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation

class ProfileUpdateForm(forms.Form):
    username = forms.CharField(max_length=100, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'id': "username",
                                                             'aria-describedby': "username-help"}))

    photo = forms.ImageField(required=False,
                             widget=forms.FileInput(attrs={'class': 'form-control',
                                                           'id': 'photo'}))

    bio = forms.CharField(max_length=199, required=False,
                          widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'id': "bio",
                                                        'aria-describedby': "bio-help"}))

    city = forms.CharField(max_length=40, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'id': "city",
                                                         'aria-describedby': "city-help"}))

    def clean_username(self):
        username = self.cleaned_data['username']

        if re.search(r'[^a-z_.1234567890-]', username):
            raise forms.ValidationError("Никнейм может состоять только из латинских букв нижнего регистра, цифр и _/-/. ")

        return username

    def clean_city(self):
        city = self.cleaned_data['city']

        if re.search(r'[^а-яА-я-]', city):
            raise forms.ValidationError("Название города может состоять только из букв и -")

        return city


CHOICES = [('Instagram', 'Instagram'),
           ('Telegram', 'Telegram'),
           ('Номер телефона', 'Номер телефона')]


class ContactCreateForm(forms.Form):
    contact = forms.CharField(max_length=100, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'id': "contact",
                                                            'aria-describedby': "city-help"}))

    contact_type = forms.CharField(widget=forms.RadioSelect(choices=CHOICES, attrs={'class': 'form-control',
                                                                                   'id': "contactType",
                                                                                   'aria-describedby': "city-help"}))

    description = forms.CharField(max_length=100, required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'id': "description",
                                                                'aria-describedby': "city-help"}))

class UserPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

