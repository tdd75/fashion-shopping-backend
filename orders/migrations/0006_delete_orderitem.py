# Generated by Django 4.1.4 on 2022-12-25 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_remove_order_amount'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]