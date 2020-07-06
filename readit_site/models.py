from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class ReaditUserModel(AbstractUser):

    def __str__(self):
        return self.username

class SubreaditModel(models.Model):
    name = models.CharField(max_length=45)
    moderator = models.OneToOneField(
        ReaditUserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.name

class SubscriptionModel(models.Model):
    user = models.ForeignKey(ReaditUserModel, on_delete=models.CASCADE)
    subreadit = models.ForeignKey(SubreaditModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} \ {self.subreadit.name}"