from .models import BookModel, AuthorModel, BookAuthorModel
from django.forms import ModelForm, TextInput, ImageField, Textarea, IntegerField, ModelMultipleChoiceField
from django import forms

class BookCreateForm(ModelForm):
    class Meta:
        model = BookModel
        fields = ['image', 'name', 'year', 'language', 'description', 'authors']

        widgets = {
            "image": (),
            "author": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Автор книги...'
            }),
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название книги...'
            }),
            "year": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Год...'
            }),
            "language": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Язык...'
            }),
            "description": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание...'
            }),
        }



