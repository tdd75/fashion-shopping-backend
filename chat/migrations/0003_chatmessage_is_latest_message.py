# Generated by Django 4.1.6 on 2023-02-11 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='is_last_message',
            field=models.BooleanField(default=False),
        ),
    ]