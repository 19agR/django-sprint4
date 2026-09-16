"""Статические страницы и обработчики ошибок сайта."""

from http import HTTPStatus

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    """Показывает информацию о проекте."""

    template_name = 'pages/about.html'


class RulesView(TemplateView):
    """Показывает правила сообщества."""

    template_name = 'pages/rules.html'


def csrf_failure(request: HttpRequest, reason: str = '') -> HttpResponse:
    """Показывает страницу отказа при проверке CSRF-токена."""
    return render(request, 'pages/403csrf.html', status=HTTPStatus.FORBIDDEN)


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Показывает страницу для несуществующего или недоступного адреса."""
    return render(request, 'pages/404.html', status=HTTPStatus.NOT_FOUND)


def server_error(request: HttpRequest) -> HttpResponse:
    """Показывает страницу внутренней ошибки сервера."""
    return render(
        request,
        'pages/500.html',
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
