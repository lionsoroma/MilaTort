# Generated by Django 2.1.2 on 2018-12-09 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20181209_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='session_key',
            field=models.CharField(blank=True, db_index=True, default=None, max_length=128, null=True, verbose_name='Ключ сесії(служова інформація)'),
        ),
    ]
