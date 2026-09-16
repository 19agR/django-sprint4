"""Модели категорий, мест, публикаций и комментариев Блогикума."""

from django.conf import settings
from django.db import models

from .constants import DISPLAY_TEXT_LENGTH, TITLE_MAX_LENGTH
from .querysets import PostQuerySet


class PublishedModel(models.Model):
    """Хранит общие признаки публикации и дату создания объекта."""

    is_published = models.BooleanField(
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
        verbose_name='Опубликовано',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    class Meta:
        """Исключает создание таблицы для абстрактной модели."""

        abstract = True


class Category(PublishedModel):
    """Описывает тематическую категорию публикаций."""

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        verbose_name='Заголовок',
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        ),
        verbose_name='Идентификатор',
    )

    class Meta:
        """Задаёт названия категории в административной панели."""

        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        """Возвращает сокращённый заголовок категории."""
        return self.title[:DISPLAY_TEXT_LENGTH]


class Location(PublishedModel):
    """Описывает место, с которым связана публикация."""

    name = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        verbose_name='Название места',
    )

    class Meta:
        """Задаёт названия местоположения в административной панели."""

        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        """Возвращает сокращённое название места."""
        return self.name[:DISPLAY_TEXT_LENGTH]


class Post(PublishedModel):
    """Хранит публикацию с автором, категорией и изображением."""

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        verbose_name='Заголовок',
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        ),
        verbose_name='Дата и время публикации',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    image = models.ImageField(
        upload_to='posts/%Y/%m/%d/',
        blank=True,
        verbose_name='Изображение',
    )

    objects = PostQuerySet.as_manager()

    class Meta:
        """Задаёт названия, обратные связи и порядок публикаций."""

        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'posts'
        ordering = ('-pub_date', '-pk')

    def __str__(self) -> str:
        """Возвращает сокращённый заголовок публикации."""
        return self.title[:DISPLAY_TEXT_LENGTH]


class Comment(models.Model):
    """Хранит комментарий пользователя к отдельной публикации."""

    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )

    class Meta:
        """Задаёт названия и порядок комментариев от старых к новым."""

        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at', 'pk')

    def __str__(self) -> str:
        """Возвращает начало текста комментария."""
        return self.text[:DISPLAY_TEXT_LENGTH]
