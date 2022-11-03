from django.shortcuts import render
from django.views import View
from books.models import BookModel
from django.db.models import Q
from users.models import Contacts
from django.contrib.auth.mixins import LoginRequiredMixin


class BookSearchView(LoginRequiredMixin, View):

    template_name = 'search/search_templ.html'
    login_url = 'login'

    def get(self, request, **kwargs):

        contact_list = []
        search_req = self.request.GET.get('search', '')

        if search_req:
            books = BookModel.objects.all().filter(Q(name__icontains=search_req) |
                                                   Q(authors__name__icontains=search_req) |
                                                   Q(description__icontains=search_req), book_type=1)
        else:
            books = None

        book_list = 0

        if books:
            for book in books:
                try:
                    buf = Contacts.objects.filter(userid=book.owner)[0]
                except:
                    buf = 0
                contact_list.append(buf)

            book_list = zip(books, contact_list)

        context = {
            'book_list': book_list,
            'search_req': search_req,
            'userid': request.user.id
        }
        print(request.user.id)
        return render(request, self.template_name, context)
