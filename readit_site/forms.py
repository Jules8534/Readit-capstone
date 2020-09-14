from django import forms
from .models import ReaditUserModel, PostModel, CommentModel
from django.contrib.auth.forms import UserCreationForm

from readit_site.models import ReaditUserModel, SubreaditModel


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


class CreateSubreaditForm(forms.ModelForm):
    name = forms.CharField(max_length=45)
    description = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField(required=False)
    video = forms.FileField(required=False)

    class Meta:
        model = SubreaditModel
        fields = ("name", "description", "image", "video")


class CommentForm(forms.ModelForm):
    # content = forms.CharField(max_length=500)
    class Meta:
        model = CommentModel
        exclude = ['post', 'user', 'created_at', 'updated_at']
