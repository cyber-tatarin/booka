from .models import BookModel, AuthorModel
from django import forms


class BookCreateForm(forms.Form):

    authors = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
                'id': 'authors_field',
                'class': 'input-book',
                'placeholder': 'Введите название авторов через запятую'
            }))
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
                'class': 'input-book',
                'placeholder': 'Введите название книги'
            }))
    year = forms.IntegerField(required=False, widget=forms.TextInput(attrs={
                'class': 'input-book',
                'placeholder': 'Введите год издания книги'
            }))
    language = forms.CharField(max_length=14, required=False, widget=forms.TextInput(attrs={
                'class': 'input-book',
                'placeholder': 'Введите язык книги'
            }))
    description = forms.CharField(max_length=400, required=False, widget=forms.Textarea(attrs={
                'class': 'input-book-description-textarea',
                'placeholder': 'Введите описание книги'
            }))

    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
                'class': 'file-input',
                'placeholder': 'Описание...',
                'name': "file",
                'id': "choose-file-container",
                'oninvalid': "this.setCustomValidity('Enter User Name Here')",
                'oninput': "this.setCustomValidity('')"
            }))


