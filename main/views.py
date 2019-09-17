from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template.response import TemplateResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from boast_auth.models import BoastUser
from .models import BoastPost
from .forms import CreatePost, CreateComment, ChangePost


@login_required
def dashboard(request):
    bps = BoastPost.objects.all()
    context = {'bps': bps}
    return render(request, 'main/dashboard.html', context)


@login_required
def home(request):
    bps = BoastPost.objects.filter(author__in=request.user.friends.all())
    context = {'bps': bps}
    return render(request, 'main/home.html', context)


@login_required
def boast_create(request):
    if request.method == 'POST':
        form = CreatePost(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            form.save()
            return redirect('boast_auth:profile')
    else:
        form = CreatePost(initial={'author': request.user.pk})
    context = {'form': form}
    return render(request, 'main/create_post.html', context)


class UserDetailView(DetailView, LoginRequiredMixin):
    model = BoastUser
    template_name = 'main/detail_user.html'
    queryset = BoastUser.objects.all()


@login_required
def subscribe_unsubscribe(request, pk):
    user = request.user
    friend = BoastUser.objects.get(pk=pk)
    if friend not in user.friends.all():
        user.friends.add(friend)
        user.save()
    else:
        user.friends.remove(friend)
        user.save()
    return redirect('main:detail_user', pk=pk)


class PostDetailView(DetailView, LoginRequiredMixin):
    model = BoastPost
    template_name = 'main/detail_post.html'
    queryset = BoastPost.objects.all()


@login_required
def detail_post(request, pk):
    bp = BoastPost.objects.get(pk=pk)
    if request.method == 'POST':
        form = CreateComment(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:detail_post', pk=bp.pk)
    else:
        form = CreateComment(initial={'owner': request.user.pk,
                                      'post': bp.pk})
    context = {'boastpost': bp, 'form': form}
    return render(request, 'main/detail_post.html', context)


@login_required
def like_post(request):
    post = get_object_or_404(BoastPost, pk=request.POST.get('post_pk'))
    if request.method == 'POST':
        if request.user not in post.likes.all():
            post.likes.add(request.user)
        else:
            post.likes.remove(request.user)
        post.save()
    return TemplateResponse(request, 'main/like.html', {'post': post})


class PostChangeView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BoastPost
    form_class = ChangePost
    template_name = 'main/change_post.html'
    queryset = BoastPost.objects.all()

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
