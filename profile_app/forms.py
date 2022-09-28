from django.forms import ModelForm
from django import forms
import re


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

        if re.search(r'[^a-z_1234567890]', username):
            raise forms.ValidationError("Никнейм может состоять только из латинских букв нижнего регистра, цифр и _ ")

        return username
