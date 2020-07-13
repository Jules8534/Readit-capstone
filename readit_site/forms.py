from django import forms
from .models import ReaditUserModel, PostModel
from django.contrib.auth.forms import UserCreationForm

# from readit_site.models import ReaditUserModel


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class ReaditUserModelForm(UserCreationForm):
    email = forms.EmailField(
        max_length=60, help_text='Required. Add a valid email address')

    class Meta:
        model = ReaditUserModel
        fields = ("email", "username", "password1", "password2")


class AddPost(forms.ModelForm):
    title = forms.CharField(max_length=150)
    content = forms.CharField(widget=forms.Textarea, max_length=500)

    class Meta:
        model = PostModel
        fields = (
            'title',
            'content',
        )
