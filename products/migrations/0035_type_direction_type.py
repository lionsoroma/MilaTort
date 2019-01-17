# Generated by Django 2.1.2 on 2019-01-07 10:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0034_auto_20190107_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='type',
            name='direction_type',
            field=models.IntegerField(default=1, help_text='Порядок показу типу(відносно категорії): менше значить вище', validators=[django.core.validators.MaxValueValidator(999), django.core.validators.MinValueValidator(0)], verbose_name='Пріорітет показу'),
            preserve_default=False,
        ),
    ]