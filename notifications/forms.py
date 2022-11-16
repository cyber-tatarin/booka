from django import forms


class NotifCreateForm(forms.Form):
    message = forms.CharField(required=True, max_length=349,
                              widget=forms.Textarea(attrs={
                                  'class': 'input-book-description-textarea',
                                  'placeholder': "Введите сообщение"}
                              ))
