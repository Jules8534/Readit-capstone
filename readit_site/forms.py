from django import forms
from .models import ReaditUserModel
from django.contrib.auth.forms import UserCreationForm

from readit_site.models import ReaditUserModel, CreateSubreaditModel

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

class ReaditUserModelForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

    class Meta:
         model = ReaditUserModel
         fields = ("email", "username", "password1", "password2")

class CreateSubreaditForm(forms.Form):

    class Meta:
        model = CreateSubreaditModel
        fields = ("title", "content", "image")