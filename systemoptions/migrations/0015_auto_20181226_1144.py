# Generated by Django 2.1.2 on 2018-12-26 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systemoptions', '0014_auto_20181226_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonestaff',
            name='phone_manager',
            field=models.DecimalField(decimal_places=0, help_text='Формат для телефонного номера: 0XXXXXXXXX (напр.: 0982548248)', max_digits=10, verbose_name='Телефонний номер менеджера:'),
        ),
    ]
