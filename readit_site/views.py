from django.shortcuts import render, reverse, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .forms import LoginForm, ReaditUserModelForm
# Create your views here.
@login_required
def index(request):
    html = "index.html"
    username = request.user.username
    return render(request, html, {"name": username})


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
    pass