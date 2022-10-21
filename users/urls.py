from django.urls import path, include
from .views import RegisterView, LoginView
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)