# Generated by Django 4.1.5 on 2023-01-23 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_items',
            field=models.JSONField(default=[]),
            preserve_default=False,
        ),
    ]
