from django.shortcuts import render, reverse, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import LoginForm, ReaditUserModelForm, CreateSubreaditForm
from .models import SubreaditModel, CreateSubreaditModel, ReaditUserModel
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
    pass

def post_view(request, subreadit, postid):
    pass


def createsubreadit_view(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    form = CreateSubreaditForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = ReaditUserModel.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form = CreateSubreaditForm()

    context['form'] = form
    return render(request, "create_subreadit", context)

def must_authenticate_view(request):
    return render(request, 'must_authenticate', ())    
