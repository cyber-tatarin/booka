from .models import BookModel, AuthorModel
from django import forms


class BookCreateForm(forms.Form):

    authors = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Автор книги...'
            }))
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название книги...'
            }))
    year = forms.IntegerField(widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Год...'
            }))
    language = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Язык...'
            }))
    description = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Описание...'
            }))

    image = forms.ImageField(required=False)



