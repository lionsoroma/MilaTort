# Generated by Django 2.1.1 on 2018-09-25 05:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(help_text='Категорія продукту. Наприклад: Торт, Фігурка, Зефір і т. д.', max_length=25, verbose_name='Категорія продукту')),
                ('category_description', models.TextField(blank=True, help_text='Опис категорії, яка відображатиметься на сайті.', max_length=256, null=True, verbose_name='Опис категорії')),
                ('accessibility', models.BooleanField(default=True, verbose_name='Доступність')),
                ('slug_category', models.SlugField(blank=True, editable=False, max_length=128, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='category_photo', verbose_name='Загальне фото для категорії')),
            ],
            options={
                'verbose_name': 'Категорія',
                'verbose_name_plural': 'Категорії',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(null=True, upload_to='products_photo', verbose_name='Фото продукту')),
                ('is_active', models.BooleanField(default=True, help_text='Дозволяє/забороняє використовувати це фото на сайті в різних розділах', verbose_name='Доступність')),
                ('land_photo', models.BooleanField(default=True, help_text='Центральне фото, яке показується зразу після загрузки', verbose_name='Стартове')),
                ('blog_photo', models.BooleanField(default=True, help_text='Фото для розділу блог', verbose_name='Блог')),
                ('slide_photo', models.BooleanField(default=True, help_text='Невеликі фото, які динамічно змініються на слайдах', verbose_name='Слайди')),
                ('dates_upload', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата загрузки')),
                ('dates_upgrade', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата останьої редакції')),
            ],
            options={
                'verbose_name': 'Фото',
                'verbose_name_plural': 'Фото',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Наявність')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Назва')),
                ('product_description', models.TextField(blank=True, help_text='Опис продукту, який відображатиметься на сайті.', max_length=128, null=True, verbose_name='Опис продукту')),
                ('slug_product', models.SlugField(blank=True, editable=False, max_length=128, null=True)),
                ('unit', models.CharField(choices=[('kg', 'кг'), ('ps', 'шт')], default='kg', max_length=2, verbose_name='КГ/ШТ')),
                ('price', models.DecimalField(decimal_places=2, default=0, help_text='Вартість за кг. чи за шт.', max_digits=6, verbose_name='Ціна за одиницю')),
                ('discount_product', models.IntegerField(default=0, help_text='Увага: знижка на продукт сумується зі знижкою клієнта. Можливі значення: 0 - 50', validators=[django.core.validators.MaxValueValidator(50), django.core.validators.MinValueValidator(0)], verbose_name='Знижка на продукт, %')),
                ('dates_add', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата додання')),
                ('dates_renovation', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата останьої редакції')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукти',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Наявність')),
                ('slug_type', models.SlugField(blank=True, editable=False, max_length=128, null=True)),
                ('typeof', models.CharField(help_text='Тип продукту відносно категорії. Наприклад: Весільний, Дитячий для торта або Банановий, Смородиновий для зефіру.', max_length=25, verbose_name='Тип продукту')),
                ('type_description', models.TextField(blank=True, help_text='Опис типу, який відображатиметься на сайті.', max_length=256, null=True, verbose_name='Опис типу')),
                ('category_plus_type', models.CharField(blank=True, help_text='Генерується автоматично! Можна редагувати якщо помітили неточність.', max_length=50, null=True, verbose_name='Категорія+Тип продукту:')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Category', verbose_name='Категорія')),
            ],
            options={
                'verbose_name': 'Тип',
                'verbose_name_plural': 'Типи',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category_plus_type_product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Type', verbose_name='Категорія+Тип'),
        ),
        migrations.AddField(
            model_name='photo',
            name='product',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Product', verbose_name='Назва продукту'),
        ),
    ]
