# Generated by Django 2.1.2 on 2018-12-11 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_remove_client_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='address',
            field=models.ForeignKey(blank=True, help_text='Адреса доставки/проживання', null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Addresses', verbose_name='Адреса'),
        ),
    ]
