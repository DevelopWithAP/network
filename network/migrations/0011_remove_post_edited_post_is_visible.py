# Generated by Django 4.0.4 on 2022-05-22 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_post_edited'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='edited',
        ),
        migrations.AddField(
            model_name='post',
            name='is_visible',
            field=models.BooleanField(default=True),
        ),
    ]
