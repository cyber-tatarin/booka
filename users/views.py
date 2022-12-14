from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View
from django.views.generic import ListView
from .forms import UserCreateForm, UserLoginForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator


User = get_user_model()


class RegisterView(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreateForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreateForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('books:book-view')

        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class LoginView(View):

    template_name = 'registration/login.html'

    def get(self, request):
        context = {
            'form': UserLoginForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserLoginForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('books:book-view')

        context = {
            'form': form
        }

        return render(request, self.template_name, context)


class UserPasswordResetView(PasswordResetView):
    template_name = "registration/password_reset_form.html"

    def get_success_url(self):
        return reverse('users:password-reset-done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"

    def get_success_url(self, request):
        return redirect(request, self.template_name)


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"

    def get_success_url(self):
        return reverse('users:password-reset-complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"

    def get_success_url(self, request):
        return redirect(request, self.template_name)