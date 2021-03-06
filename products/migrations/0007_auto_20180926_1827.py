# Generated by Django 2.1.1 on 2018-09-26 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20180926_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Вартість за кг. чи за шт.', max_digits=7, verbose_name='Ціна за одиницю чи за кг.'),
        ),
    ]
