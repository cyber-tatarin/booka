from django.shortcuts import render
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Q
from django.contrib.auth import get_user_model
from .forms import ProfileUpdateForm
from users.models import Cities

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
    template_name = 'profile_app/profile_upd.html'

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

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

            curr_city = Cities.objects.get_or_create(
                city=data['city'].title,
                defaults={'city': data['city'].title}
            )

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
