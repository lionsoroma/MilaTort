# Generated by Django 2.1.2 on 2018-11-24 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_comment_client_commit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='commit',
        ),
        migrations.AddField(
            model_name='comment',
            name='r_commit',
            field=models.CharField(blank=True, help_text='Ваш коментар', max_length=256, null=True, verbose_name='Відгук / коментар'),
        ),
    ]
