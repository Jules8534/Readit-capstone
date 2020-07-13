from django.shortcuts import render, reverse, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import LoginForm, ReaditUserModelForm, AddPost
from .models import SubreaditModel, PostModel, ReaditUserModel
# Create your views here.


@login_required
def index(request):
    html = "index.html"
    username = request.user.username
    subreadits = SubreaditModel.objects.all()
    return render(
        request, html,
        {
            "name": username,
            "subreadits": subreadits,
        }
    )


def login_view(request):
    html = "loginform.html"

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
            return HttpResponseRedirect(
                request.GET.get('next', reverse('homepage'))
            )
    form = LoginForm()
    return render(request, html, {"form": form})


# https://simpleisbetterthancomplex.com/tips/2016/08/04/django-tip-9-password-change-form.html
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('homepage'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


@login_required
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


def readitusermodel_view(request):
    context = {}
    if request.POST:
        form = ReaditUserModelForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=password)
            login(request, account)
            return redirect('homepage')
        else:  # GET request
            context['readitusermodel_form'] = form
    else:
        form = ReaditUserModelForm()
        context['readitusermodel_form'] = form
    return render(request, 'register.html', context)


def subreadit_view(request, subreadit):
    try:
        subreadit = SubreaditModel.objects.get(name=subreadit)
    except SubreaditModel.DoesNotExist:
        return HttpResponseRedirect(reverse('homepage'))

    posts = subreadit.postmodel_set.all()
    return render(request, 'subreadit.html', {"subreadit": subreadit, "posts": posts})


@login_required
def post_view(request, subreadit, user_id):
    if request.method == 'POST':
        form = AddPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return HttpResponseRedirect('add_post', pk=post.pk)
        else:
            form = AddPost()

    # if request.method == 'POST':
    #     form = AddPost(request.POST)
    # if form.is_valid():
    #     data = form.cleaned_data
    #     all_user = ReaditUserModel.objects.all()
    #     user = ReaditUserModel.objects.get(id=user_id)
    #     post = PostModel.objects.create(
    #         post=data['post'],
    #         author=user,
    #     )
        return render(request, 'subreadit.html', {'form': form})


def createsubreadit_view(request):
    pass
