from django.urls import path
from .views import NotifCreateView, NotifList


app_name = 'notification'
urlpatterns = [

    path('<int:pk>/', NotifCreateView.as_view(), name='notif-create'), #добавить второй аргумент инт бук
    path('box/', NotifList.as_view(), name='notif-list'),

    ]
