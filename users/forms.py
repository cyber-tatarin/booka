from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django import forms
import re
from typing import Dict, Final, Optional
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.handlers.wsgi import WSGIRequest
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(max_length=254,
                             error_messages={'required': 'lola.',
                                             'invalid': 'raaaa'},
                             widget=forms.EmailInput({
                                 'required': True,
                                 'class': 'input-book',
                                 'placeholder': 'Введите email'
                             }))

    username = forms.CharField(max_length=15, required=True,
                               widget=forms.TextInput(attrs={'class': 'input-book',
                                                             'placeholder': 'Введите никнейм',
                                                             }))

    password1 = forms.CharField(max_length=100, required=True,
                                widget=forms.PasswordInput(attrs={'class': 'input-book',
                                                                  'placeholder': 'Введите пароль'}))

    password2 = forms.CharField(max_length=100, required=True,
                                widget=forms.PasswordInput(attrs={'class': 'input-book',
                                                                  'placeholder': 'Повторите пароль'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']

        if re.search(r'[^a-z_1234567890]', username):
            raise forms.ValidationError("Никнейм может состоять только из латинских букв нижнего регистра, цифр и _ ")
        return username


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'Неправильный логин или пароль'
        super().__init__(*args, **kwargs)

    username = forms.CharField(max_length=20, required=True,
                               widget=forms.TextInput(attrs={'class': 'input-book',
                                                             'placeholder': 'Введите никнейм'}))

    password = forms.CharField(max_length=100, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'input-book',
                                                             'placeholder': 'Введите пароль'}))


# Constants for sending password-reset emails.

PASSWORD_RESET_FORM_TEMPLATE: Final[str] = "registration/password_reset_form.html"
PASSWORD_RESET_HTML_TEMPLATE: Final[str] = "registration/password_reset_email.html"
PASSWORD_RESET_TEXT_TEMPLATE: Final[str] = "registration/password_reset_email.txt"
PASSWORD_RESET_SUBJECT_TEMPLATE: Final[str] = "registration/password_reset_subject.txt"
SUPPORT_EMAIL: Final[str] = "Email"
FROM_EMAIL: Final[str] = f"BOOKA Support <{SUPPORT_EMAIL}>"

class UserPasswordResetForm(PasswordResetForm):

    def save(
            self,
            domain_override: Optional[str] = None,
            subject_template_name: str = PASSWORD_RESET_SUBJECT_TEMPLATE,
            email_template_name: str = PASSWORD_RESET_TEXT_TEMPLATE,
            use_https: Optional[bool] = None,
            token_generator: PasswordResetTokenGenerator = default_token_generator,
            from_email: Optional[str] = FROM_EMAIL,
            request: Optional[WSGIRequest] = None,
            html_email_template_name: Optional[str] = PASSWORD_RESET_HTML_TEMPLATE,
            extra_email_context: Optional[Dict[str, str]] = None
    ) -> None:

        email_template_name = PASSWORD_RESET_TEXT_TEMPLATE
        from_email = FROM_EMAIL
        html_email_template_name = PASSWORD_RESET_HTML_TEMPLATE
        subject_template_name = PASSWORD_RESET_SUBJECT_TEMPLATE

        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        UserModel = get_user_model()
        email_field_name = UserModel.get_email_field_name()  # type: ignore

        for user in self.get_users(email):
            user_email = getattr(user, email_field_name)
            context = {
                'email': user_email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }

            self.send_mail(
                subject_template_name=subject_template_name,
                email_template_name=email_template_name,
                context=context,
                from_email=from_email,
                to_email=user_email,
                html_email_template_name=html_email_template_name
            )