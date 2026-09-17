"""Формы публикаций, комментариев и редактирования профиля."""

from django import forms
from django.contrib.auth import get_user_model

from .constants import COMMENT_TEXTAREA_ROWS, PUBLICATION_DATETIME_FORMAT
from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Позволяет автору заполнить содержимое публикации."""

    class Meta:
        """Исключает выбор автора и задаёт виджет даты публикации."""

        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                format=PUBLICATION_DATETIME_FORMAT,
                attrs={'type': 'datetime-local'},
            ),
        }


class CommentForm(forms.ModelForm):
    """Позволяет пользователю ввести только текст комментария."""

    class Meta:
        """Исключает изменение автора и публикации через форму."""

        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': COMMENT_TEXTAREA_ROWS}),
        }


class ProfileForm(forms.ModelForm):
    """Позволяет изменить публичные данные и почту своего профиля."""

    class Meta:
        """Ограничивает форму несистемными полями пользователя."""

        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email')
