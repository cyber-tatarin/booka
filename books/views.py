from django.shortcuts import render
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Q
from django.contrib.auth import get_user_model
from .forms import BookCreateForm
from .models import BookModel, AuthorModel, BookAuthorModel
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseNotFound



class BookListView(View):
    login_url = 'login'
    template_name = 'books/books.html'

    def get(self, request, **kwargs):
        books = BookModel.objects.all().filter(owner=request.user.id)
        authors = AuthorModel.objects.all()
        context = {
            'book_list': books,
            'author_list': authors
        }

        return render(request, self.template_name, context)



class BookCreateView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'books/books_create.html'

    def get(self, request, **kwargs):

        form = BookCreateForm(request.POST, request.FILES)

        context = {
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request):

        form = BookCreateForm(request.POST, request.FILES)

        if form.is_valid():


            form.save()
            return redirect('books:book-view')

        context = {
            'form': form
        }

        return render(request, self.template_name, context)



class BookUpdateView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'books/books_update.html'

    def get(self, request, **kwargs):

        book = get_object_or_404(BookModel, id=self.kwargs.get('pk'))
        authors = AuthorModel.objects.all()
        form = BookCreateForm(initial={
            'image': book.image,
            'authors': book.authors,
            'name': book.name,
            'year': book.year,
            'language': book.language,
            'description': book.description
        })

        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = BookCreateForm(data=request.POST, files=request.FILES)
        book = get_object_or_404(BookModel, id=self.kwargs.get('pk'))

        if form.is_valid():
            data = form.cleaned_data
            book.name = data['name']
            book.year = data['year']
            book.authors = data['authors']
            book.language = data['language']
            book.description = data['description']
            if data['image']:
                book.image = data['image']
            book.save()
            return redirect('books:book-view')

        context = {
            'form': form
        }

        return render(request, self.template_name, context)



class BookDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'

    def get_queryset(self):
        queryset = BookModel.objects.all().filter(owner=self.request.user, id=self.kwargs.get('pk'))
        return queryset

    def get_success_url(self):
        return reverse('books:book-view')

    def get_template_names(self):
        return 'books/books_delete.html'










