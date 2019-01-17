# Generated by Django 2.1.2 on 2018-10-11 19:00

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0020_auto_20181005_1301'),
        ('main', '0004_auto_20181011_1819'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, editable=False, help_text='Всі знижки враховані', max_digits=10, verbose_name='Загальна вартість кошика')),
                ('notes', models.TextField(blank=True, help_text='Побажання до заказу', max_length=256, null=True, verbose_name='Нотатки для кошика')),
                ('date_of_readiness', models.DateTimeField(default=datetime.datetime.now, help_text='На коли має бути готоаий заказ: дата і час', verbose_name='Готовність на(дата):')),
                ('delivery_required', models.BooleanField(blank=True, default=False, help_text='Саму доставку потрібно вибирати як окремий продукт', null=True, verbose_name='Потібна доставка?')),
                ('dates_basket', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата оформлення')),
                ('update_basket', models.DateTimeField(auto_now=True, null=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='basket_of_client', to='main.Client', verbose_name='Клієнт')),
            ],
            options={
                'verbose_name': 'Кошик',
                'verbose_name_plural': 'Кошики',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_description', models.TextField(blank=True, help_text='Опис заказу', max_length=128, null=True, verbose_name='Опис заказу')),
                ('weight_or_pcs', models.DecimalField(blank=True, decimal_places=1, default=1, help_text='Бажана вага чи кількість шт.', max_digits=5, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Вага чи кількість')),
                ('unitof', models.CharField(blank=True, choices=[('kg', 'кг'), ('ps', 'шт')], default='kg', max_length=2, verbose_name='КГ/ШТ')),
                ('price_per_item', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Якщо не вводити в це поле жодних даних, то цінна підтягнеться з БД ', max_digits=10, verbose_name='Ціна за од.')),
                ('discount_total', models.IntegerField(blank=True, default=0, editable=False, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='Суми знижок, %')),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, default=0, editable=False, max_digits=10, verbose_name='Сума зі знижками')),
                ('dates_order', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата оформлення')),
                ('update_order', models.DateTimeField(auto_now=True, null=True)),
                ('session_key', models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='Ключ сесії(служова інформація)')),
                ('present_in_basket', models.BooleanField(blank=True, default=True, help_text='Заказ зберігаєть в списку заказів навіть тоді, коли клієнт його видалив.Використовується для статистики. В кошик він не попадає!', null=True, verbose_name='Присутність в корзині')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Client', verbose_name='Клієнт')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Закази',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current', models.CharField(blank=True, default=None, max_length=24, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статуси',
            },
        ),
        migrations.AddField(
            model_name='basket',
            name='orders',
            field=models.ManyToManyField(related_name='orders_in_basket', to='orders.Order', verbose_name='Закази в кошику'),
        ),
    ]