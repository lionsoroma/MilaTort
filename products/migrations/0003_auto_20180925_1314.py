# Generated by Django 2.1.1 on 2018-09-25 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='category_description',
        ),
        migrations.AddField(
            model_name='category',
            name='motto',
            field=models.CharField(blank=True, help_text='Гасло категорії, яке відображатиметься на сайті.(Максимальна довжина 48 символів)', max_length=48, null=True, verbose_name='Гасло категорії'),
        ),
    ]
