# Generated by Django 2.1.2 on 2018-11-28 10:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_comment_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(blank=True, help_text='Оцінка продукту: залишає клієнт, макс. значення - 10 од.', null=True, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)], verbose_name='Оцінка продукту'),
        ),
    ]