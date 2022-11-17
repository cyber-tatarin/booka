from django.shortcuts import render
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Q
from django.contrib.auth import get_user_model
from .forms import ProfileUpdateForm, ContactCreateForm, UserPasswordChangeForm
from users.models import Cities, Contacts
from books.models import BookModel
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect

User = get_user_model()


class ProfileBooksView(LoginRequiredMixin, View):

    login_url = 'login'
    template_name = 'profile_app/profilebooks_templ.html'

    def get(self, request, **kwargs):
        s_user = get_object_or_404(User, id=kwargs['pk'])
        books = BookModel.objects.all().filter(owner=s_user, book_type=1)
        context = {
            'searched_user': s_user,
            'check_id': request.user.id,
            'books': books
        }
        return render(request, self.template_name, context)


class ProfileWishView(LoginRequiredMixin, View):

    login_url = 'login'
    template_name = 'profile_app/profilewish_templ.html'

    def get(self, request, **kwargs):
        s_user = get_object_or_404(User, id=kwargs['pk'])
        books = BookModel.objects.all().filter(owner=s_user, book_type=2)

        context = {
            'searched_user': s_user,
            'check_id': request.user.id,
            'books': books
        }
        return render(request, self.template_name, context)


class ProfileContactsView(LoginRequiredMixin, View):

    login_url = 'login'
    template_name = 'profile_app/profilecontacts_templ.html'

    def get(self, request, **kwargs):
        s_user = get_object_or_404(User, id=kwargs['pk'])
        contacts = Contacts.objects.all().filter(userid=s_user)

        context = {
            'searched_user': s_user,
            'check_id': request.user.id,
            'contacts': contacts
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
                   'photo': curr_user.photo,
                   'userid': request.user.id}

        return render(request, self.template_name, context)

    def post(self, request):
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

            return redirect(f'/profile/books/{request.user.id}')

        context = {
            'form': form,
            'photo': curr_user.photo,
            'userid': request.user.id
        }

        return render(request, self.template_name, context)


class SettingsView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'profile_app/settings.html'

    def get_context_data(self, **kwargs):
        ctx = {
            'userid': self.request.user.id
        }
        return ctx


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

            try:
                next = self.request.POST.get('next')
                return HttpResponseRedirect(next)
            except:
                return redirect('profile_app:profilecontacts_templ')

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
            'contacts': queryset,
            'userid': request.user.id
        }

        return render(request, self.template_name, context)


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'

    def get_queryset(self):
        queryset = Contacts.objects.all().filter(userid=self.request.user, id=self.kwargs.get('pk'))
        return queryset

    def get_success_url(self):
        try:
            next = self.request.POST.get('next')
            return str(next)
        except:
            return reverse('profile_app:profilecontacts_templ')

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

            try:
                next = self.request.POST.get('next')
                return HttpResponseRedirect(next)
            except:
                return redirect('profile_app:profilecontacts_templ')

        context = {
            'form': form
        }

        return render(request, self.template_name, context)

    def get_object(self):
        return get_object_or_404(Contacts, pk=self.kwargs.get('pk'))


class UserPasswordChangeView(PasswordChangeView):

    form_class = UserPasswordChangeForm
    template_name = 'profile_app/password_change.html'
    success_message = 'Ваш пароль был успешно изменён!'

    def get_success_url(self):
        return reverse('profile_app:password-change-done')


class UserPasswordChangeDoneView(PasswordChangeView):
    template_name = 'profile_app/password_change_done.html'

    def get_success_url(self, request):
        return redirect(request, self.template_name)


class TechnicalSupportView(View):
    template_name = 'profile_app/technical_support.html'

    def get(self, request):
        context = {
            'userid': request.user.id
        }
        return render(request, self.template_name, context)
