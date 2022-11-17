from .models import BookModel, AuthorModel
from django import forms
import re
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import datetime


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
    year = forms.IntegerField(max_value=datetime.datetime.now().year, required=False, widget=forms.NumberInput(attrs={
                'class': 'input-book',
                'placeholder': 'Введите год издания книги'
            }))
    language = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
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

    def clean_authors(self):
        authors = self.cleaned_data['authors']

        if re.search(r'[^а-яА-Яa-zA-Z-,. ]', authors):
            raise forms.ValidationError(
                "Имя автора может состоять из букв русского и английского алфавита, символов -,. ")

        return authors

    def clean_name(self):
        name = self.cleaned_data['name']

        if re.search(r'[^а-яА-Яa-zA-Z-,.+!?#$%()/@ ]', name):
            raise forms.ValidationError(
                "Имя книги может состоять из букв русского и английского алфавита, символов -,.+!?#$%()/@")

        return name

    def clean_description(self):
        description = self.cleaned_data['description']

        if re.search(r'[^а-яА-Яa-zA-Z-,.()%$#@!&*?+=/;:"0123456789 ]', description):
            raise forms.ValidationError(
                "Описание может состоять из букв русского и английского алфавита, цифр, символов -,.()%$#@!&*?+=/;:")

        return description

    def clean_language(self):
        language = self.cleaned_data['language']

        if re.search(r'[^а-яА-Яa-zA-Z-,. ]', language):
            raise forms.ValidationError(
                "Язык может состоять из букв русского и английского алфавита, -,.")

        return language

    def clean_year(self):
        year = self.cleaned_data['year']
        if year == '':
            year = 0
            return year
        year_int = int(year)
        cur_year = datetime.datetime.now().year
        if re.search(r'\d\d\d\d\d', year):
            raise forms.ValidationError(
                "Год может состоять только из цифр (максимум 4 цифры)!")

        if year_int > cur_year or year_int < 0:
            raise forms.ValidationError(
                "Год не может быть больше текущего и меньше 0")

        return year

