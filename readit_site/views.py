from django.shortcuts import render, reverse, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .validators import validate_subreadit
from .forms import LoginForm, ReaditUserModelForm, AddPost, CreateSubreaditForm, CommentForm
from .models import SubreaditModel, ReaditUserModel, PostModel, SubscriptionModel, CommentModel, PostVoteModel, CommentVoteModel
# Create your views here.


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['name'] = self.request.user.username
        context['subreadits'] = SubreaditModel.objects.all()
        if self.get_posts():
            context['posts'] = self.get_posts()
        return context

    def get_posts(self):
        subscriptions = SubscriptionModel.objects.filter(
            user=self.request.user)
        posts = PostModel.objects.none()
        for sub in subscriptions:
            posts = posts.union(sub.subreadit.postmodel_set.all())

        if posts:
            posts = posts.order_by('-created_at')
            return posts


# @login_required
# def index(request):
#     html = "index.html"

#     username = request.user.username
#     subreadits = SubreaditModel.objects.all()
#     context = {'name': username, 'subreadits': subreadits}

#     subscriptions = SubscriptionModel.objects.filter(user=request.user)
#     posts = PostModel.objects.none()
#     for sub in subscriptions:
#         posts = posts.union(sub.subreadit.postmodel_set.all())

#     if posts:
#         posts = posts.order_by('-created_at')
#         context['posts'] = posts

#     return render(request, html, context)

class LoginView(TemplateView):
    template_name = "loginform.html"

    def get_context_data(self, *args, **kwargs):
        context = super(LoginView, self).get_context_data(*args, **kwargs)
        context['form'] = LoginForm()
        return context

    # GET, POST, PUT, DELETE
    # if request.method === 'post'
    # def post()

    def post(self, request):
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


# def login_view(request):
#     html = "loginform.html"

#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             user = authenticate(
#                 request, username=data['username'], password=data['password'])
#             if user:
#                 login(request, user)
#             return HttpResponseRedirect(
#                 request.GET.get('next', reverse('homepage'))
#             )
#     form = LoginForm()
#     return render(request, html, {"form": form})


# https://simpleisbetterthancomplex.com/tips/2016/08/04/django-tip-9-password-change-form.html

class ChangePasswordView(LoginRequiredMixin, TemplateView):
    template_name = 'change_password.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(ChangePasswordView, self).get_context_data(*args, **kwargs)
        context['form'] = PasswordChangeForm(self.request.user)
        return context

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('homepage'))
        else:
            messages.error(request, 'Please correct the error below.')


# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)
#             messages.success(
#                 request, 'Your password was successfully updated!')
#             return HttpResponseRedirect(reverse('homepage'))
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'change_password.html', {
#         'form': form
#     })


@login_required
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


def readitusermodel_view(request):
    if request.POST:
        form = ReaditUserModelForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=password)
            login(request, account)
            return redirect('homepage')

    return render(request, 'register.html', {'form': ReaditUserModelForm()})


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

    form = AddPost(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.subreadit = subreadit_obj
        post.save()
        post.url = reverse('post', args=[subreadit, post.id])
        post.save()

    context['form'] = form
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
def post_view(request, subreadit, postid):
    try:
        sub = SubreaditModel.objects.get(name=subreadit)
        post = PostModel.objects.get(id=postid)
    except SubreaditModel.DoesNotExist:
        return HttpResponseRedirect(reverse('homepage'))
    except PostModel.DoesNotExist:
        return HttpResponseRedirect(reverse('subreadit', args=[subreadit]))

    comments = post.commentmodel_set.all()
    comment_data = {}
    for comment in comments:
        votes = comment.commentvotemodel_set.all()
        upVotes = votes.filter(is_upVote=True)
        downVotes = votes.filter(is_upVote=False)

        count_upVotes = upVotes.count()
        count_downVotes = downVotes.count()
        can_upVote = not upVotes.filter(user=request.user).exists()
        can_downVote = not downVotes.filter(user=request.user).exists()
        comment_data[comment.id] = {'upVotes': count_upVotes, 'downVotes': count_downVotes,
                                    'can_upVote': can_upVote, 'can_downVote': can_downVote}

    votes = post.postvotemodel_set.all()
    upVotes = votes.filter(is_upVote=True)
    downVotes = votes.filter(is_upVote=False)

    count_upVotes = upVotes.count()
    count_downVotes = downVotes.count()
    can_upVote = not upVotes.filter(user=request.user).exists()
    can_downVote = not downVotes.filter(user=request.user).exists()
    votes = {'upVotes': count_upVotes, 'downVotes': count_downVotes,
             'can_upVote': can_upVote, 'can_downVote': can_downVote}

    context = {'sub': sub, 'post': post, 'comments': comments,
               'comment_data': comment_data, 'votes': votes}

    form = CommentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        data = form.cleaned_data
        comment = CommentModel.objects.create(
            post=post,
            user=request.user,
            content=data['content'])
        form = CommentForm()

    context['form'] = form
    context['is_moderator'] = sub.moderator == request.user
    return render(request, 'post.html', context) if post.subreadit == sub else HttpResponseRedirect(reverse('subreadit', args=[subreadit]))


@login_required
def post_action(request, subreadit, postid, action):
    try:
        post = PostModel.objects.get(id=postid)
    except PostModel.DoesNotExist:
        return HttpResponseRedirect(reverse('homepage'))

    if action == 'upvote' or action == 'downvote':
        is_upVote = True if action == 'upvote' else False
        post_query = PostVoteModel.objects.filter(
            user=request.user, post=post, is_upVote=is_upVote)
        if post_query.exists():
            post_query.first().delete()
        else:
            PostVoteModel.objects.create(
                user=request.user, post=post, is_upVote=is_upVote)
        return HttpResponseRedirect(reverse('post', args=[subreadit, postid]))
    elif action == 'delete':
        subreadit_obj = SubreaditModel.objects.get(name=subreadit)
        if subreadit_obj.moderator == request.user:
            post.delete()
        return HttpResponseRedirect(reverse('subreadit', args=[subreadit]))
    else:
        return HttpResponseRedirect(reverse('homepage'))


@login_required
def comment_action(request, subreadit, postid, commentid, action):
    try:
        comment = CommentModel.objects.get(id=commentid)
    except CommentModel.DoesNotExist:
        return HttpResponseRedirect(reverse('homepage'))

    if action == 'upvote' or action == 'downvote':
        is_upVote = True if action == 'upvote' else False
        comment_query = CommentVoteModel.objects.filter(
            user=request.user, comment=comment, is_upVote=is_upVote)
        if comment_query.exists():
            comment_query.first().delete()
        else:
            CommentVoteModel.objects.create(
                user=request.user, comment=comment, is_upVote=is_upVote)
        return HttpResponseRedirect(reverse('post', args=[subreadit, postid]))
    elif action == 'delete':
        subreadit_obj = SubreaditModel.objects.get(name=subreadit)
        if subreadit_obj.moderator == request.user:
            comment.delete()
        return HttpResponseRedirect(reverse('post', args=[subreadit, postid]))
    else:
        return HttpResponseRedirect(reverse('homepage'))


@login_required
def createsubreadit_view(request):
    context = {}
    user = request.user

    form = CreateSubreaditForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        validation = validate_subreadit(form)
        if validation == True:
            obj = form.save(commit=False)
            obj.moderator = user
            obj.save()
            return HttpResponseRedirect(reverse('subreadit', args=[form.cleaned_data['name']]))
        else:
            context['errors'] = validation

    context['form'] = form
    context['name'] = request.user.username
    return render(request, "create_subreadit.html", context)


@login_required
def delete_post(request, postid=None):
    post_to_delete = PostModel.objects.get(id=postid)
    post_to_delete.delete()
    return HttpResponseRedirect(reverse('subreadit', args=[subreadit]))
