from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import LoginForm, ReaditUserModelForm, AddPost, CreateSubreaditForm
from .models import SubreaditModel, ReaditUserModel, PostModel, SubscriptionModel
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
    context = {}
    try:
        subreadit_obj = SubreaditModel.objects.get(name=subreadit)
        context["subreadit"] = subreadit_obj
        subscription = SubscriptionModel.objects.get(
            user=request.user, subreadit=subreadit_obj)
        context["subscription"] = True
    except SubreaditModel.DoesNotExist:
        return HttpResponseRedirect(reverse('homepage'))
    except SubscriptionModel.DoesNotExist:
        context["subscription"] = False

    context["posts"] = subreadit_obj.postmodel_set.all()
    context["subscribe_link"] = reverse("subscribe", args=[subreadit])

    if request.method == 'POST':
        form = AddPost(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post = PostModel.objects.create(
                title=data['title'],
                content=data['content'],
                user=request.user,
                subreadit=subreadit_obj,
            )
    context['form'] = AddPost()
    return render(request, 'subreadit.html', context)


@login_required
def subreadit_subscribe(request, subreadit):
    try:
        subreadit_obj = SubreaditModel.objects.get(name=subreadit)
        subscription = SubscriptionModel.objects.get(
            user=request.user, subreadit=subreadit_obj)
        subscription.delete()
    except SubreaditModel.DoesNotExist:
        return HttpResponseRedirect(reverse('homepage'))
    except SubscriptionModel.DoesNotExist:
        SubscriptionModel.objects.create(
            user=request.user, subreadit=subreadit_obj)

    return HttpResponseRedirect(reverse('subreadit', args=[subreadit]))


@login_required
def post_view(request, subreadit, user_id):
    pass


@login_required
def createsubreadit_view(request):
    context = {}
    user = request.user

    # form = CreateSubreaditForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        form = CreateSubreaditForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.moderator = user
            obj.save()
            # data = form.cleaned_data
            # sub = SubreaditModel.objects.create(name=data['name'], description=data["description"], moderator=request.user)
        else:
            print(form.errors)
    else:
        print(f"Method: {request.method}")
    form = CreateSubreaditForm()

    context['form'] = form
    context['name'] = request.user.username
    return render(request, "create_subreadit.html", context)
