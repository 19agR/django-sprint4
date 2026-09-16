"""Конфигурация приложения блога."""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Задаёт имя приложения и тип первичного ключа моделей."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = 'Блог'
