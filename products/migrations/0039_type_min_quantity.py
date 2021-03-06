# Generated by Django 2.1.2 on 2019-02-15 12:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0038_auto_20190128_0922'),
    ]

    operations = [
        migrations.AddField(
            model_name='type',
            name='min_quantity',
            field=models.IntegerField(default=1, help_text='Мінімальна кількість шт чи кг, яку можна замовити. Вказується для типу продуктів в цілому.', validators=[django.core.validators.MaxValueValidator(999), django.core.validators.MinValueValidator(1)], verbose_name='Мінімально можлива кількість до замовлення:'),
        ),
    ]
