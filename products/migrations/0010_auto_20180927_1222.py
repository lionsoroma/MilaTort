# Generated by Django 2.1.1 on 2018-09-27 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_remove_type_price_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug_product',
            field=models.SlugField(blank=True, editable=False, max_length=128, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='type',
            name='slug_type',
            field=models.SlugField(blank=True, editable=False, max_length=128, null=True, unique=True),
        ),
    ]
