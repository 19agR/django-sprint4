# Блогикум — Django Sprint 4

Продолжение проекта Sprint 3 на Python 3.11 и Django 5.1.1.

В проекте реализованы регистрация, вход, выход, изменение и восстановление
пароля, профили пользователей, публикации с изображениями и комментарии.
Автор может редактировать и удалять собственные записи. Удаление требует
подтверждения. Главная страница, профиль и категория выводят по 10 публикаций
на страницу с количеством комментариев.

Скрытые и отложенные публикации доступны автору в его профиле и по прямой
ссылке. Остальные посетители видят только опубликованные записи, дата которых
уже наступила и категория которых не скрыта. Категории и местоположения
создаются через административную панель.

## Локальный запуск в Windows PowerShell

Из корня репозитория:

```powershell
py -3.11 -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe blogicum\manage.py migrate
.\venv\Scripts\python.exe blogicum\manage.py runserver
```

Сайт доступен по адресу <http://127.0.0.1:8000/>.

При необходимости загрузите готовые демонстрационные данные:

```powershell
.\venv\Scripts\python.exe blogicum\manage.py loaddata db.json
```

Для доступа к административной панели создайте суперпользователя:

```powershell
.\venv\Scripts\python.exe blogicum\manage.py createsuperuser
```

## Проверка

В репозитории используются предоставленные тесты Практикума:

```powershell
.\venv\Scripts\python.exe -m pytest
.\venv\Scripts\python.exe blogicum\manage.py check
.\venv\Scripts\python.exe blogicum\manage.py makemigrations --check --dry-run
.\venv\Scripts\python.exe -m flake8 blogicum --jobs=1
```

Строгая проверка оформления, включая докстринги и миграции:

```powershell
.\venv\Scripts\python.exe -m flake8 blogicum --isolated --jobs=1 --max-line-length=79 --max-complexity=10 --ignore=W503,D203,D213,D401
```

## Настройки и файлы

Готовые шаблоны Практикума перенесены в `blogicum/templates/` без изменения
содержимого. Статические страницы используют классы `TemplateView`.
Обработчики ошибок подключены для 403 CSRF, 404 и 500; страницы 404 и 500
отображаются вместо отладочных страниц при `DEBUG = False`.

Письма восстановления пароля сохраняются файловым бэкендом в
`blogicum/sent_emails/`, изображения — в `blogicum/media/`.
Эти директории, локальная база SQLite и виртуальное окружение исключены из Git.
В настройках используются русский язык и часовой пояс `Europe/Moscow`.
