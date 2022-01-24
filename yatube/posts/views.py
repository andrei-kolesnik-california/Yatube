from django.http.response import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import Post, Group, Comment, Follow
from .forms import PostForm, CommentForm

POSTS_PER_PAGE = 10


def index(request: HttpRequest) -> HttpResponse:
    """Получение списка постов из базы данных."""
    post_list = Post.objects.all()
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'posts/index.html', context)


def group_posts(request: HttpRequest, slug: str) -> HttpResponse:
    """Получение списка постов из базы данных для указанной группы."""
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, 'posts/group_list.html', context)


def profile(request: HttpRequest, username: str) -> HttpResponse:
    """Получение списка постов из базы данных для указанного пользователя."""
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author__username=username)
    posts_number = posts.count()
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    following = None
    if request.user.is_authenticated:
        if Follow.objects.filter(user=request.user, author=author).exists():
            following = True
        else:
            following = False
    context = {
        'author': author,
        'page_obj': page_obj,
        'posts_number': posts_number,
        'following': following
    }
    return render(request, 'posts/profile.html', context)


@login_required
def post_create(request: HttpRequest) -> HttpResponse:
    """Создание нового поста."""
    is_edit = False
    groups = Group.objects.all()
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=post.author.username)

    context = {
        'form': form,
        'groups': groups,
        'is_edit': is_edit
    }

    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request: HttpRequest, post_id: int) -> HttpResponse:
    """Редактирование поста."""
    is_edit = True
    post = get_object_or_404(Post, pk=post_id)
    groups = Group.objects.all()
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if request.method == 'POST' and form.is_valid():
        post.save()
        return redirect('posts:post_detail', post_id=post.pk)

    context = {
        'form': form,
        'groups': groups,
        'is_edit': is_edit
    }

    return render(request, 'posts/create_post.html', context)


def post_detail(request, post_id):
    """Получение выбранного поста из базы данных."""
    post = get_object_or_404(Post, pk=post_id)
    username = post.author.username
    posts_number = Post.objects.filter(author__username=username).count()
    comments = Comment.objects.filter(post_id=post_id)
    form = CommentForm(request.POST or None)
    context = {
        'posts_number': posts_number,
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """Получение списка выбранных постов из базы данных."""
    post_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = User.objects.get(username=username)
    if request.user != author and not Follow.objects.filter(
            user=request.user, author=author).exists():
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('posts:profile', username=username)
