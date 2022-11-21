from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View
from django.views.generic import ListView
from .forms import UserCreateForm, UserLoginForm, UserPasswordResetForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
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
    email_template_name = "registration/password_reset_email.html"
    extra_email_context = None
    form_class = UserPasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("users:password-reset-done")
    template_name = "registration/password_reset_form.html"
    title = _("Password reset")
    token_generator = default_token_generator

    def get_success_url(self):
        return reverse('users:password-reset-done')

class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"
    title = _("Password reset sent")

    def get_success_url(self, request):
        return redirect(request, self.template_name)