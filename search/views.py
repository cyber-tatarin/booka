from django.shortcuts import render
from django.views import View
from books.models import BookModel
from django.db.models import Q


class BookSearchView(View):

    template_name = 'search/search_templ.html'

    def get(self, request, **kwargs):

        search_req = self.request.GET.get('search', '')

        if search_req:
            queryset = BookModel.objects.all().filter(Q(name__icontains=search_req) |
                                                      Q(authors__name__icontains=search_req) |
                                                      Q(description__icontains=search_req))
        else:
            queryset = None

        context = {
            'search_res': queryset,
            'search_req': search_req
        }
        return render(request, self.template_name, context)
