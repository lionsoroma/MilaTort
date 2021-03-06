# Generated by Django 2.1.1 on 2018-09-30 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20180930_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='blog_photo',
            field=models.BooleanField(default=True, help_text='Фото для розділу блог. Вимоги: співвідношення сторін 16:10, інакше зображення буде обрізано!', verbose_name='Блог'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='land_photo',
            field=models.BooleanField(default=True, help_text='Центральне фото, яке показується зразу після загрузки. Вимоги: співвідношення сторін 16:9, інакше зображення буде обрізано!', verbose_name='Стартове'),
        ),
    ]
