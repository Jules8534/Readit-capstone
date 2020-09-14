from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from readit_site.models import *
# Register your models here.

# https://stackoverflow.com/questions/9443863/register-every-table-class-from-an-app-in-the-django-admin-page
models = (
    SubreaditModel,
    SubscriptionModel,
    PostModel,
    CommentModel,
    PostVoteModel,
    CommentVoteModel,
)

admin.site.register(ReaditUserModel, UserAdmin)
admin.site.register(models)
