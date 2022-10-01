from django.shortcuts import render
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Q
from django.contrib.auth import get_user_model
from .forms import NotifCreateForm
from .models import Notifications

User = get_user_model()


class NotifCreateView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'notifications/create_notif.html'

    def get(self, request, **kwargs):

        if request.user.id == kwargs['pk']:
            return redirect('notification:notif-list')

        receiver = get_object_or_404(User, id=kwargs['pk'])
        # добавить подтверждение, что такая книга существует

        form = NotifCreateForm()

        context = {
            'form': form,
        }

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = NotifCreateForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            receiver = get_object_or_404(User, id=kwargs['pk'])
            notif = Notifications(message=data['message'],
                                  sender=request.user,
                                  receiver=receiver,
                                  ntype=request.POST['ntype'])
            notif.save()

            return redirect(f'/profile/{receiver.id}')

        context = {
            'form': form,
        }

        return render(request, self.template_name, context)


class NotifList(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'notifications/list_notif.html'

    def get(self, request, **kwargs):

        received = Notifications.objects.all().filter(receiver=request.user)
        sent = Notifications.objects.all().filter(sender=request.user)

        context = {
            'received': received,
            'sent': sent
        }

        return render(request, self.template_name, context)

