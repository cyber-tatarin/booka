from django import forms


class NotifCreateForm(forms.Form):
    message = forms.CharField(max_length=349,
                              widget=forms.Textarea(attrs={
                                  'class': 'form-control',
                                  'id': "message",
                                  'aria-describedby': "username-help"}
                              ))
