"""Уточняет название заголовка категории."""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Уточняет название заголовка категории."""

    dependencies = [
        ('blog', '0002_alter_category_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Заголовок'),
        ),
    ]
