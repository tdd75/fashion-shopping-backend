# Generated by Django 4.1.6 on 2023-02-08 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_remove_order_order_items_and_more"),
        ("cart", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="order",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="orders.order",
            ),
        ),
    ]