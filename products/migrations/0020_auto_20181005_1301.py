# Generated by Django 2.1.1 on 2018-10-05 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_auto_20181005_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Вартість за кг. чи за шт.', max_digits=7, verbose_name='Ціна за одиницю чи за кг.'),
        ),
    ]
