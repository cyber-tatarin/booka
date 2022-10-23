from django.urls import path
from .views import NotifCreateView, SentNotifList, ReceivedNotifList


app_name = 'notification'
urlpatterns = [

    path('<int:pk>/<int:bookid>/', NotifCreateView.as_view(), name='notif-create'), #добавить второй аргумент инт бук
    path('sent/', SentNotifList.as_view(), name='sent-notif-list'),
    path('received/', ReceivedNotifList.as_view(), name='received-notif-list'),

    ]
