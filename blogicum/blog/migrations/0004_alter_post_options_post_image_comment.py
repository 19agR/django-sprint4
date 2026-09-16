"""Добавляет изображения, комментарии и порядок публикаций."""

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    """Добавляет изображения, комментарии и порядок публикаций."""

    dependencies = [
        ('blog', '0003_alter_category_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={
                'default_related_name': 'posts',
                'ordering': ('-pub_date', '-pk'),
                'verbose_name': 'публикация',
                'verbose_name_plural': 'Публикации'
            },
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True,
                                    upload_to='posts/%Y/%m/%d/',
                                    verbose_name='Изображение'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id',
                 models.BigAutoField(auto_created=True,
                                     primary_key=True,
                                     serialize=False,
                                     verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('created_at',
                 models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')),
                ('author',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='comments',
                                   to=settings.AUTH_USER_MODEL,
                                   verbose_name='Автор комментария')),
                ('post',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='comments',
                                   to='blog.post',
                                   verbose_name='Публикация')),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('created_at', 'pk'),
            },
        ),
    ]
