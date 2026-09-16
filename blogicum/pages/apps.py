"""Конфигурация приложения статических страниц."""

from django.apps import AppConfig


class PagesConfig(AppConfig):
    """Задаёт имя приложения и тип первичного ключа моделей."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
    verbose_name = 'Страницы'
