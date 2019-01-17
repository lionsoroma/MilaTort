# Generated by Django 2.1.2 on 2018-12-02 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_auto_20181128_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_stuff_plus',
            field=models.BooleanField(default=True, help_text='Якщо так, тобуде можливість вибрати начинку/серединку при оформленні заказу', verbose_name='Доступність начинки/серединки'),
        ),
        migrations.AlterField(
            model_name='product',
            name='cooking_time',
            field=models.DurationField(blank=True, help_text='Час виготовлення. Величина приблизна і використовується для розрахунку терміну приблизного виконання замовлення (відображаються лише години !!!)', null=True, verbose_name='Час виготовлення'),
        ),
    ]
