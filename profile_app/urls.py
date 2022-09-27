from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import ProfileView, ProfileUpdateView


app_name = 'profile_app'
urlpatterns = [

    path('<int:pk>', ProfileView.as_view(), name='profile'),
    path('update/', ProfileUpdateView.as_view(), name='profile-update')
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)