# Generated by Django 2.2 on 2020-01-21 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dojoreads_app', '0005_auto_20200121_1521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='rating',
        ),
    ]
