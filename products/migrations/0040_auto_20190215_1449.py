# Generated by Django 2.1.2 on 2019-02-15 12:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0039_type_min_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='type',
            name='min_quantity',
            field=models.IntegerField(blank=True, default=1, help_text='Мінімальна кількість шт чи кг, яку можна замовити. Вказується для типу продуктів в цілому.Значення по замовчуванню: 1', null=True, validators=[django.core.validators.MaxValueValidator(999), django.core.validators.MinValueValidator(1)], verbose_name='Мінімально можлива кількість до замовлення:'),
        ),
    ]
