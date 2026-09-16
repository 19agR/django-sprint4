"""Выборки публикаций с учётом доступности и связанных данных."""

from typing import Self

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.utils import timezone


class PostQuerySet(models.QuerySet):
    """Предоставляет общие правила выборки публикаций."""

    def published(self) -> Self:
        """Возвращает наступившие публикации из открытых категорий."""
        return self.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )

    def visible_to(self, user: AbstractBaseUser | AnonymousUser) -> Self:
        """Дополняет открытые публикации всеми записями их автора."""
        published_posts = self.published()
        if user.is_authenticated:
            return published_posts | self.filter(author=user)
        return published_posts

    def with_related(self) -> Self:
        """Загружает автора, категорию и место вместе с публикацией."""
        return self.select_related('author', 'category', 'location')

    def with_comment_count(self) -> Self:
        """Добавляет число комментариев для карточек публикаций."""
        return self.with_related().annotate(
            comment_count=models.Count('comments'),
        ).order_by(*self.model._meta.ordering)
