from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.


class ReaditUserModel(AbstractUser):

    def __str__(self):
        return self.username


class SubreaditModel(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField(default="")
    moderator = models.ForeignKey(ReaditUserModel, on_delete=models.CASCADE)
    date_published = models.DateTimeField(
        auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="date updated")
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    # slug = models.SlugField(blank=True, unique=True)
    video = models.FileField(
        upload_to='uploads/videos/', blank=True, null=True)

    def __str__(self):
        return self.name


class SubscriptionModel(models.Model):
    user = models.ForeignKey(ReaditUserModel, on_delete=models.CASCADE)
    subreadit = models.ForeignKey(SubreaditModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} \ {self.subreadit.name}"


class PostModel(models.Model):
    subreadit = models.ForeignKey(SubreaditModel, on_delete=models.CASCADE)
    user = models.ForeignKey(ReaditUserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.CharField(max_length=500)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CommentModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    user = models.ForeignKey(ReaditUserModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostVoteModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    user = models.ForeignKey(ReaditUserModel, on_delete=models.CASCADE)
    is_upVote = models.BooleanField()


class CommentVoteModel(models.Model):
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE)
    user = models.ForeignKey(ReaditUserModel, on_delete=models.CASCADE)
    is_upVote = models.BooleanField()
