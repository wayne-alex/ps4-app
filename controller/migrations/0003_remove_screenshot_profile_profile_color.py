# Generated by Django 5.1.1 on 2024-10-06 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller', '0002_remove_game_total_playtime_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='screenshot',
            name='profile',
        ),

    ]
