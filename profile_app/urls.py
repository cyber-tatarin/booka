from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import ProfileBooksView, ProfileUpdateView, SettingsView, ContactCreateView, \
    ContactListView, ContactDeleteView, ContactUpdateView, ProfileContactsView, ProfileWishView


app_name = 'profile_app'
urlpatterns = [

    path('books/<int:pk>', ProfileBooksView.as_view(), name='books-profile'),
    path('contacts/<int:pk>', ProfileContactsView.as_view(), name='contacts-profile'),
    path('wish/<int:pk>', ProfileWishView.as_view(), name='wish-profile'),
    path('update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('settings/contacts/create', ContactCreateView.as_view(), name='contact-create'),
    path('settings/contacts/list', ContactListView.as_view(), name='contact-list'),
    path('settings/contacts/delete/<int:pk>', ContactDeleteView.as_view(), name='contact-delete'),
    path('settings/contacts/update/<int:pk>', ContactUpdateView.as_view(), name='contact-update')

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
