from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'books'

urlpatterns = [
    path('', views.BookListView.as_view(), name='book-view'),
    path('create/<int:type>', views.BookCreateView.as_view(), name='book-create'),
    path('update/<int:pk>/', views.BookUpdateView.as_view(), name='book-update'),
    path('delete/<int:pk>/<int:type>', views.BookDeleteView.as_view(), name='book-delete'),
    path('wish/', views.WishBookListView.as_view(), name='wish-book-view'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)