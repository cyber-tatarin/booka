from django.forms import ModelForm
from django import forms
import re
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.core.exceptions import ValidationError
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

class UserPasswordChangeForm(forms.Form):

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }

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

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })