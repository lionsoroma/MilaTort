# Generated by Django 2.1.2 on 2018-11-08 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_auto_20181005_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='disclaimer_is_visible',
            field=models.BooleanField(default=False, help_text='Застереження для категорії, відображатиметься на сайті, коли активувати', verbose_name='Застереження<br/>показувати/<br/>не показувати'),
        ),
    ]
