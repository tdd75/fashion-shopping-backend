# Generated by Django 4.1.4 on 2023-01-08 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_types', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producttype',
            old_name='available',
            new_name='quantity',
        ),
    ]
