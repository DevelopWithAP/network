# Generated by Django 4.0.4 on 2022-05-18 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_alter_user_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='edited',
            field=models.BooleanField(default=False),
        ),
    ]
