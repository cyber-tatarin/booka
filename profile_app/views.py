from django.shortcuts import render
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Q
from django.contrib.auth import get_user_model
from .forms import ProfileUpdateForm, ContactCreateForm
from users.models import Cities, Contacts
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


class ProfileView(View):
    template_name = 'profile_app/profile_templ.html'

    def get(self, request, **kwargs):
        s_user = get_object_or_404(User, id=kwargs['pk'])
        current_user_id = request.user.id

        context = {
            'searched_user': s_user,
            'check_id': current_user_id
        }
        return render(request, self.template_name, context)


class ProfileUpdateView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'profile_app/profile_upd.html'

    def get(self, request, **kwargs):

        curr_user = get_object_or_404(User, id=request.user.id)

        if curr_user.city:
            form = ProfileUpdateForm(initial={'username': curr_user.username,
                                              'bio': curr_user.bio,
                                              'city': curr_user.city.city
                                              })

        else:
            form = ProfileUpdateForm(initial={'username': curr_user.username,
                                              'bio': curr_user.bio
                                              })

        context = {'form': form,
                   'photo': curr_user.photo}

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = ProfileUpdateForm(data=request.POST, files=request.FILES)
        curr_user = get_object_or_404(User, id=request.user.id)

        if form.is_valid():
            data = form.cleaned_data
            curr_user.username = data['username']
            curr_user.bio = data['bio']

            if data['city']:
                titledcity = data['city'].upper()

                curr_city = Cities.objects.get_or_create(city=titledcity)
                curr_user.city = curr_city[0]

            if data['photo']:
                curr_user.photo = data['photo']
            curr_user.save()

            return redirect(f'/profile/{request.user.id}')

        context = {
            'form': form,
            'photo': curr_user.photo
        }

        return render(request, self.template_name, context)


class SettingsView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'profile_app/settings.html'


class ContactCreateView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'profile_app/contact_create.html'

    def get(self, request, **kwargs):
        form = ContactCreateForm()

        context = {
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = ContactCreateForm(data=request.POST)

        if form.is_valid():
            data = form.cleaned_data
            contact = Contacts(**data)
            contact.userid = request.user
            contact.save()
            return redirect('profile_app:settings')

        context = {
            'form': form
        }

        return render(request, self.template_name, context)


class ContactListView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'profile_app/contact_list.html'

    def get(self, request, **kwargs):
        queryset = Contacts.objects.all().filter(userid=request.user.id)
        context = {
            'contact_list': queryset
        }

        return render(request, self.template_name, context)


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'

    def get_queryset(self):
        queryset = Contacts.objects.all().filter(userid=self.request.user, id=self.kwargs.get('pk'))
        return queryset

    def get_success_url(self):
        return reverse('profile_app:contact-list')

    def get_template_names(self):
        return 'profile_app/contact_delete.html'


class ContactUpdateView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'profile_app/contact_upd.html'

    def get(self, request, **kwargs):
        contact = self.get_object()
        form = ContactCreateForm(initial={
            'contact_type': contact.contact_type,
            'contact': contact.contact,
            'description': contact.description
        })

        context = {
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = ContactCreateForm(data=request.POST)
        contact = self.get_object()

        if form.is_valid():
            data = form.cleaned_data
            contact.contact = data['contact']
            contact.contact_type = data['contact_type']
            contact.description = data['description']
            contact.save()
            return redirect('profile_app:contact-list')

        context = {
            'form': form
        }

        return render(request, self.template_name, context)

    def get_object(self):
        return get_object_or_404(Contacts, pk=self.kwargs.get('pk'))
