# Generated by Django 2.1.2 on 2018-12-23 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systemoptions', '0002_auto_20181223_1344'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailstaff',
            options={'verbose_name': 'Email менеджера', 'verbose_name_plural': 'Emails менеджерів'},
        ),
        migrations.AlterModelOptions(
            name='emailwebservice',
            options={'verbose_name': 'Параметри поштового клієнта', 'verbose_name_plural': 'Параметри поштових клієнтів'},
        ),
        migrations.AlterModelOptions(
            name='phonestaff',
            options={'verbose_name': 'Телефонний номер менеджера', 'verbose_name_plural': 'Телефонні номера менеджерів'},
        ),
        migrations.AlterField(
            model_name='emailwebservice',
            name='email_use_tls',
            field=models.CharField(choices=[(True, 'True'), (False, 'False')], default=True, max_length=5, verbose_name='EMAIL_USE_TLS'),
        ),
        migrations.AlterField(
            model_name='systemoptions',
            name='phone_send',
            field=models.BooleanField(blank=True, default=True, help_text='Якщо відміченно, то на всі телефонні номери, що виділенні нижче будуть вілісланні СМС про новий заказУВАГА! Послуга платна! По СМС неможливо відправити повну інформацію про заказ: тому рекомендується використовувавти в парі з Email інформуванням', null=True, verbose_name='Розсилати СМС при отриманні заказу?'),
        ),
    ]
