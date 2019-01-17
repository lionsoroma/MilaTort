# Generated by Django 2.1.1 on 2018-10-05 10:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_category_direction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='direction',
            field=models.IntegerField(help_text='Порядок показу категорії: менше значить вище', unique=True, validators=[django.core.validators.MaxValueValidator(999), django.core.validators.MinValueValidator(0)], verbose_name='Пріорітет показу категорії'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=1, default=0, help_text='Вартість за кг. чи за шт.', max_digits=7, verbose_name='Ціна за одиницю чи за кг.'),
        ),
    ]
