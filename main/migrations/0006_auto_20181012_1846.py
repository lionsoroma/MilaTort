# Generated by Django 2.1.2 on 2018-10-12 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20181012_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(blank=True, help_text='Номер телефону', max_length=28, null=True, verbose_name='Номер телефону'),
        ),
    ]
