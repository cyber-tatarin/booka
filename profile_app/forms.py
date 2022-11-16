from django.forms import ModelForm
from django import forms
import re
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm


class ProfileUpdateForm(forms.Form):
    username = forms.CharField(max_length=100, required=True,
                               widget=forms.TextInput(attrs={'class': 'input-book',
                                                             'placeholder': 'Введите никнейм'}))

    photo = forms.ImageField(required=False,
                             widget=forms.FileInput(attrs={'class': 'file-input',
                                                           'name': "file",
                                                           'id': "choose-file-container", }))

    bio = forms.CharField(max_length=199, required=False,
                          widget=forms.Textarea(attrs={'class': 'input-book-description-textarea',
                                                        'placeholder': 'Введите описание профиля'}))

    city = forms.CharField(max_length=40, required=False,
                           widget=forms.TextInput(attrs={'class': 'input-book',
                                                         'placeholder': 'Введите свой город'}))

    def clean_bio(self):
        bio = self.cleaned_data['bio']

        if re.search(r'[^а-яА-Яa-zA-Z-,.()%$#@!&*?+=/;:"0123456789 ]', bio):
            raise forms.ValidationError(
                "Описание может состоять из букв русского и английского алфавита, цифр, символов -,.()%$#@!&*?+=/;:")

        return bio

    def clean_username(self):
        username = self.cleaned_data['username']

        if re.search(r'[^a-z_.1234567890-]', username):
            raise forms.ValidationError(
                "Никнейм может состоять только из латинских букв нижнего регистра, цифр и _/-/. ")

        return username

    def clean_city(self):
        city = self.cleaned_data['city']

        if re.search(r'[^а-яА-Яa-zA-Z-]', city):
            raise forms.ValidationError("Название города может состоять только из букв русского и английского алфавита и -")

        return city


CHOICES = [('Instagram', 'Instagram'),
           ('Telegram', 'Telegram'),
           ('Номер телефона', 'Номер телефона')]


class ContactCreateForm(forms.Form):
    contact = forms.CharField(max_length=100, required=True,
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

    def clean_contact(self):
        contact = self.cleaned_data['contact']

        if re.search(r'[^а-яА-Яa-zA-Z-,.()#@+/:0123456789 ]', contact):
            raise forms.ValidationError(
                "Контакт может состоять из букв русского и английского алфавита, цифр, символов -,.()#@+/:")

        return contact

    def clean_description(self):
        description = self.cleaned_data['description']

        if re.search(r'[^а-яА-Яa-zA-Z-,.()%$#@!&*?+=/;:"0123456789 ]', description):
            raise forms.ValidationError(
                "Описание может состоять из букв русского и английского алфавита, цифр, символов -,.()%$#@!&*?+=/;:")

        return description


class UserPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True,
                   'class': 'input-book',
                   'placeholder': 'Введите свой старый пароль'
                   }
        ),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          'class': 'input-book',
                                          'placeholder': 'Введите новый пароль'
                                          }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          'class': 'input-book',
                                          'placeholder': 'Повторите новый пароль'
                                          }),
    )
