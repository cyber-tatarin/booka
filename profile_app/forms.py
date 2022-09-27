from django.forms import ModelForm
from django import forms


class ProfileUpdateForm(forms.Form):
    username = forms.CharField(max_length=100, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'id': "username",
                                                             'aria-describedby': "username-help"}))

    photo = forms.ImageField(required=False,
                             widget=forms.FileInput(attrs={'class': 'form-control',
                                                           'id': 'photo'}))

    bio = forms.CharField(max_length=100, required=True,
                          widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'id': "bio",
                                                        'aria-describedby': "bio-help"}))

    city = forms.CharField(max_length=100, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'id': "city",
                                                         'aria-describedby': "city-help"}))
