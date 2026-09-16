"""Настройки управления блогом через административную панель."""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Category, Comment, Location, Post

User = get_user_model()
admin.site.unregister(User)


class PostInline(admin.TabularInline):
    """Показывает публикации в форме редактирования их автора."""

    model = Post
    extra = 0
    show_change_link = True


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Дополняет стандартную панель пользователя его публикациями."""

    inlines = (PostInline,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настраивает поиск и управление видимостью категорий."""

    list_display = ('title', 'slug', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_published',)
    search_fields = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Настраивает поиск и управление видимостью местоположений."""

    list_display = ('name', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Настраивает поиск, фильтрацию и публикацию записей."""

    list_display = ('title', 'pub_date', 'author', 'is_published')
    list_filter = ('is_published', 'category', 'pub_date')
    search_fields = ('title', 'text')
    list_select_related = ('category', 'location', 'author')
    date_hierarchy = 'pub_date'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Настраивает просмотр и поиск комментариев пользователей."""

    list_display = ('text', 'author', 'post', 'created_at')
    search_fields = ('text', 'author__username')
    list_select_related = ('author', 'post')
