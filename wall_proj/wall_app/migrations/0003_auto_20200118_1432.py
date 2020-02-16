# Generated by Django 2.2 on 2020-01-18 22:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wall_app', '0002_auto_20200118_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='messages',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='users',
        ),
        migrations.RemoveField(
            model_name='message',
            name='users',
        ),
        migrations.AddField(
            model_name='comment',
            name='message',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='wall_app.Message'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='wall_app.User'),
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message', to='wall_app.User'),
        ),
    ]
