from django.shortcuts import render
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Q
from django.contrib.auth import get_user_model
from .forms import BookCreateForm
from .models import BookModel, AuthorModel
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseNotFound
import re
from users.models import Contacts


class BookListView(LoginRequiredMixin, View):

    login_url = 'login'
    template_name = 'books/books.html'

    def get(self, request, **kwargs):
        contact_list = []
        books = BookModel.objects.all().filter(book_type=1)
        if books:
            for book in books:
                try:
                    buf = Contacts.objects.filter(userid=book.owner)[0]
                except:
                    buf = 0
                contact_list.append(buf)

        context = {
            'book_list': zip(books, contact_list),
            'current_user': request.user,
            'type': 1
        }

        return render(request, self.template_name, context)


class BookCreateView(LoginRequiredMixin, View):

    login_url = 'login'
    template_name = 'books/books_create.html'

    def get(self, request, **kwargs):

        form = BookCreateForm()

        context = {
            'form': form,
            'type': kwargs['type'],
            'userid': request.user.id
        }

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        form = BookCreateForm(request.POST, request.FILES)

        if form.is_valid():

            data = form.cleaned_data
            book = BookModel(name=data['name'],
                             year=data['year'],
                             language=data['language'],
                             description=data['description'],
                             owner=request.user,
                             book_type=kwargs['type']
                             )

            if data['image']:
                book.image = data['image']

            book.save()

            upper_author_str = data['authors'].upper()
            upper_author_list = re.split(' , |, |,', upper_author_str)

            for author in upper_author_list:
                buf = AuthorModel.objects.get_or_create(name=author)
                book.authors.add(buf[0])

            try:
                next = request.POST.get('next')
                return HttpResponseRedirect(next)
            except:
                return redirect('books:book-view')

        context = {
            'form': form,
            'userid': request.user.id
        }

        return render(request, self.template_name, context)


class BookUpdateView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'books/books_update.html'

    def get(self, request, **kwargs):

        authors_list = []

        book = get_object_or_404(BookModel, id=self.kwargs.get('pk'), owner=request.user, book_type=1)
        authors_query_list = book.authors.all()

        for author in authors_query_list:
            authors_list.append(author.name)
        authors = ', '.join(authors_list)

        form = BookCreateForm(initial={
            'image': book.image,
            'authors': authors,
            'name': book.name,
            'year': book.year,
            'language': book.language,
            'description': book.description
        })

        context = {
            'form': form,
            'userid': request.user.id,
            'title': book.name
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        form = BookCreateForm(data=request.POST, files=request.FILES)
        book = get_object_or_404(BookModel, id=self.kwargs.get('pk'), owner=request.user, book_type=1)

        if form.is_valid():
            data = form.cleaned_data
            book.name = data['name']
            book.year = data['year']

            book.language = data['language']
            book.description = data['description']

            if data['image']:
                book.image = data['image']

            upper_author_str = data['authors'].upper()
            upper_author_list = re.split(' , |, |,', upper_author_str)
            book.authors.clear()

            for author in upper_author_list:
                buf = AuthorModel.objects.get_or_create(name=author)
                book.authors.add(buf[0])

            book.save()

            try:
                next = request.POST.get('next')
                return HttpResponseRedirect(next)
            except:
                return redirect('books:book-view')

        context = {
            'form': form,
            'userid': request.user.id
        }

        return render(request, self.template_name, context)


class BookDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'

    def get_queryset(self):
        queryset = BookModel.objects.all().filter(owner=self.request.user, id=self.kwargs.get('pk'))
        return queryset

    def get_success_url(self):
        try:
            next = self.request.POST.get('next')
            return str(next)
        except:
            return redirect('books:book-view')

    def get_template_names(self):
        return 'books/books_delete.html'


class WishBookListView(LoginRequiredMixin, View):

    login_url = 'login'
    template_name = 'books/wish_books.html'

    def get(self, request, **kwargs):
        books = BookModel.objects.all().filter(book_type=2, owner=request.user)

        context = {
            'book_list': books,
            'userid': request.user.id,
            'type': 2
        }

        return render(request, self.template_name, context)
