#!/usr/bin/env python
"""Командная утилита управления проектом Блогикум."""

import os
import sys


def main() -> None:
    """Запускает административную команду Django из аргументов терминала."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogicum.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            'Не удалось импортировать Django. Установите зависимости '
            'и активируйте виртуальное окружение проекта.'
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
