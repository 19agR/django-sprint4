"""Вспомогательные функции отображения публикаций."""

from django.core.paginator import Page, Paginator
from django.db.models import QuerySet
from django.http import HttpRequest

from .constants import POSTS_PER_PAGE
from .models import Post


def paginate_posts(
    request: HttpRequest,
    posts: QuerySet[Post],
    per_page: int = POSTS_PER_PAGE,
) -> Page:
    """Возвращает страницу публикаций по параметру запроса page."""
    paginator = Paginator(posts, per_page)
    return paginator.get_page(request.GET.get('page'))
