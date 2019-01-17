# Generated by Django 2.1.1 on 2018-10-02 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20181002_0822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='disclaimer',
            field=models.TextField(blank=True, help_text='Застереження для категорії, відображатиметься на сайті, коли активувати', max_length=256, null=True, verbose_name='Текст застереження'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug_category',
            field=models.SlugField(blank=True, editable=False, max_length=128, null=True, unique=True),
        ),
    ]