# Generated by Django 4.1.5 on 2023-01-26 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0004_alter_address_phone'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='address',
            constraint=models.UniqueConstraint(condition=models.Q(('is_default', True)), fields=('is_default',), name='only_one_default_address'),
        ),
    ]