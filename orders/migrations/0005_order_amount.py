# Generated by Django 4.1.7 on 2023-02-22 21:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_remove_order_order_items_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
    ]
