# Generated by Django 2.1.2 on 2018-11-08 19:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20181108_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='date_of_readiness',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 8, 19, 45, 0, 817142, tzinfo=utc), help_text='На коли має бути готоаий заказ: дата і час', verbose_name='Готовність на(дата):'),
        ),
    ]
