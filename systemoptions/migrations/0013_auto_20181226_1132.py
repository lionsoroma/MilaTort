# Generated by Django 2.1.2 on 2018-12-26 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systemoptions', '0012_auto_20181226_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonestaff',
            name='phone_manager',
            field=models.CharField(help_text='Формат для телефонного номера: 0XXXXXXXXX (напр.: 0982548248)', max_length=10, verbose_name='Телефонний номер менеджера:'),
        ),
    ]