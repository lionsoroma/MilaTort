# Generated by Django 2.1.2 on 2018-12-02 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_auto_20181202_1227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_stuff_plus',
        ),
    ]
