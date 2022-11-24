from django.shortcuts import render
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Q
from django.contrib.auth import get_user_model
from .forms import NotifCreateForm
from .models import Notifications
from books.models import BookModel
from users.models import Contacts
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from booka.settings import EMAIL_HOST_USER

User = get_user_model()


class NotifCreateView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'notifications/create_notif.html'

    def get(self, request, **kwargs):

        if request.user.id == kwargs['pk']:
            return redirect('books:book-view')

        receiver = get_object_or_404(User, id=kwargs['pk'])
        book = get_object_or_404(BookModel, id=kwargs['bookid'])

        form = NotifCreateForm()

        context = {
            'form': form,
            'receiver': receiver,
            'book': book,
            'userid': request.user.id
        }

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = NotifCreateForm(data=request.POST)

        book = get_object_or_404(BookModel, id=kwargs['bookid'])

        if form.is_valid():
            data = form.cleaned_data
            receiver = get_object_or_404(User, id=kwargs['pk'])
            notif = Notifications(message=data['message'],
                                  sender=request.user,
                                  receiver=receiver,
                                  book=book)
            notif.save()

            send_mail(
                f'Booka: Вы получили сообщение насчет книги "{book}"',
                f'Приветствуем! Вы сообщение насчет книги "{book}" от пользователя {request.user.username}! \n \n'
                f'Вот, что букер пишет Вам: {data["message"]}. \n \n'
                f'Зайдите на буку, чтобы ответить http://booka.pythonanywhere.com/',
                EMAIL_HOST_USER,
                [receiver.email],
                fail_silently=True,
            )

            try:
                next = request.POST.get('next')
                return HttpResponseRedirect(next)
            except:
                return redirect('books:book-view')

        context = {
            'form': form,
        }

        return render(request, self.template_name, context)


class SentNotifList(LoginRequiredMixin, View):

    login_url = 'login'
    template_name = 'notifications/sent_list_notif.html'

    def get(self, request, **kwargs):

        contact_list = []
        sent = Notifications.objects.all().filter(sender=request.user).order_by('-time')
        sent_list = 0

        if sent:
            for notif in sent:
                try:
                    buf = Contacts.objects.filter(userid=notif.receiver)[0]
                except:
                    buf = 0
                contact_list.append(buf)

            sent_list = zip(sent, contact_list)

        context = {
            'sent': sent_list,
            'userid': request.user.id
        }

        return render(request, self.template_name, context)


class ReceivedNotifList(LoginRequiredMixin, View):

    login_url = 'login'
    template_name = 'notifications/received_list_notif.html'

    def get(self, request, **kwargs):

        contact_list = []

        received = Notifications.objects.all().filter(receiver=request.user).order_by('-time')
        received_list = 0

        if received:
            for notif in received:
                try:
                    buf = Contacts.objects.filter(userid=notif.sender)[0]
                except:
                    buf = 0
                contact_list.append(buf)

            received_list = zip(received, contact_list)

        context = {
            'received': received_list,
            'userid': request.user.id
        }

        return render(request, self.template_name, context)
