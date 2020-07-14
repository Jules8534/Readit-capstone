from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class ReaditUserModel(AbstractUser):

    def __str__(self):
        return self.username

class SubreaditModel(models.Model):
    name = models.CharField(max_length=45)
    moderator = models.ForeignKey(ReaditUserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SubscriptionModel(models.Model):
    user = models.ForeignKey(ReaditUserModel, on_delete=models.CASCADE),
    subreadit = models.ForeignKey(SubreaditModel, on_delete=models.CASCADE),

    def __str__(self):
        return f"{self.user.username} \ {self.subreadit.name}"

class PostModel(models.Model):
    subreadit = models.ForeignKey(SubreaditModel, on_delete=models.CASCADE),
    user = models.ForeignKey(ReaditUserModel, on_delete=models.CASCADE),
    title = models.CharField(max_length=150)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CommentModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE),
    user = models.ForeignKey(ReaditUserModel, on_delete=models.CASCADE),
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PostVoteModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    user = models.ForeignKey(ReaditUserModel, on_delete=models.CASCADE)

class CommentVoteModel(models.Model):
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE)
    user = models.ForeignKey(ReaditUserModel, on_delete=models.CASCADE)

class CreateSubreaditModel(models.Model):
    title   = models.CharField(max_length=50, null=False, blank=False)
    content = models.TextField(max_length=5000, null=False, blank=False)
    image   = models.ImageField(upload_to=upload_location, null=False, blank=False)
    date_published = models.DateTimeField(auto_now_add=True, verbase_name="date published")
    date_updated   = models.DateTimeField(auto_now=True, verbase_name="date updated")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

