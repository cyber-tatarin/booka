from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404



class HomeView(TemplateView):
    template_name = 'lh/home.html'
