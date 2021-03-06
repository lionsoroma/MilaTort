# Generated by Django 2.1.2 on 2019-01-07 11:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0035_type_direction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='type',
            name='direction_type',
            field=models.IntegerField(help_text='Порядок показу типу(відносно категорії): менше значить вище', unique=True, validators=[django.core.validators.MaxValueValidator(999), django.core.validators.MinValueValidator(0)], verbose_name='Пріорітет показу'),
        ),
    ]
