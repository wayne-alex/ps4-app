# Generated by Django 5.1.1 on 2024-10-06 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='total_playtime',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='total_playtime',
        ),

    ]
