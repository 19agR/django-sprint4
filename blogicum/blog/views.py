"""Представления публикаций, профилей и комментариев Блогикума."""

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .forms import CommentForm, PostForm, ProfileForm
from .models import Category, Comment, Post
from .utils import paginate_posts

User = get_user_model()


def index(request: HttpRequest) -> HttpResponse:
    """Показывает страницу последних доступных публикаций."""
    posts = Post.objects.published().with_comment_count()
    return render(request, 'blog/index.html', {
        'page_obj': paginate_posts(request, posts),
    })


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """Показывает опубликованные записи открытой категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    posts = category.posts.published().with_comment_count()
    return render(request, 'blog/category.html', {
        'category': category,
        'page_obj': paginate_posts(request, posts),
    })


def profile(request: HttpRequest, username: str) -> HttpResponse:
    """Показывает профиль и доступные посетителю записи пользователя."""
    author = get_object_or_404(User, username=username)
    posts = author.posts.visible_to(request.user).with_comment_count()
    return render(request, 'blog/profile.html', {
        'profile': author,
        'page_obj': paginate_posts(request, posts),
    })


@login_required
@require_http_methods(['GET', 'POST'])
def edit_profile(request: HttpRequest) -> HttpResponse:
    """Редактирует профиль только текущего пользователя."""
    form = ProfileForm(
        request.POST or None,
        instance=request.user,
    )
    if form.is_valid():
        user = form.save()
        return redirect('blog:profile', username=user.username)
    return render(request, 'blog/user.html', {'form': form})


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """Показывает доступную публикацию и её комментарии."""
    post = get_object_or_404(
        Post.objects.visible_to(request.user).with_related(),
        pk=post_id,
    )
    return render(request, 'blog/detail.html', {
        'post': post,
        'form': CommentForm(),
        'comments': post.comments.select_related('author'),
    })


@login_required
@require_http_methods(['GET', 'POST'])
def create_post(request: HttpRequest) -> HttpResponse:
    """Создаёт публикацию от имени текущего пользователя."""
    form = PostForm(
        request.POST or None,
        request.FILES or None,
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def edit_post(request: HttpRequest, post_id: int) -> HttpResponse:
    """Редактирует публикацию, перенаправляя посторонних к просмотру."""
    post = get_object_or_404(Post, pk=post_id)
    if post.author_id != request.user.pk:
        return redirect('blog:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post,
    )
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/create.html', {'form': form})


@login_required
@require_http_methods(['GET', 'POST'])
def delete_post(request: HttpRequest, post_id: int) -> HttpResponse:
    """Удаляет свою публикацию после подтверждения POST-запросом."""
    post = get_object_or_404(Post.objects.with_related(), pk=post_id)
    if post.author_id != request.user.pk:
        return redirect('blog:post_detail', post_id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {
        'form': PostForm(instance=post),
    })


@login_required
@require_POST
def add_comment(request: HttpRequest, post_id: int) -> HttpResponse:
    """Добавляет комментарий к доступной пользователю публикации."""
    post = get_object_or_404(
        Post.objects.visible_to(request.user).with_related(),
        pk=post_id,
    )
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


@login_required
@require_http_methods(['GET', 'POST'])
def edit_comment(
    request: HttpRequest,
    post_id: int,
    comment_id: int,
) -> HttpResponse:
    """Редактирует свой комментарий к указанной в адресе публикации."""
    comment = get_object_or_404(
        Comment,
        pk=comment_id,
        post_id=post_id,
        author=request.user,
    )
    form = CommentForm(
        request.POST or None,
        instance=comment,
    )
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', {
        'comment': comment,
        'form': form,
    })


@login_required
@require_http_methods(['GET', 'POST'])
def delete_comment(
    request: HttpRequest,
    post_id: int,
    comment_id: int,
) -> HttpResponse:
    """Удаляет свой комментарий после подтверждения POST-запросом."""
    comment = get_object_or_404(
        Comment,
        pk=comment_id,
        post_id=post_id,
        author=request.user,
    )
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', {'comment': comment})
