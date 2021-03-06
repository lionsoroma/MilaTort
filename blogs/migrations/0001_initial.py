# Generated by Django 2.1.1 on 2018-09-25 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commit', models.TextField(blank=True, help_text='Ваш коментар', max_length=256, null=True, verbose_name='Відгук / коментар')),
                ('dates_commit', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата')),
                ('dates_edit', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата останьої редакції')),
                ('product_commit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Product', verbose_name='Відгук до продукту / події')),
            ],
            options={
                'verbose_name': 'Відгук / коментар',
                'verbose_name_plural': 'Відгуки / коментарі',
            },
        ),
    ]
