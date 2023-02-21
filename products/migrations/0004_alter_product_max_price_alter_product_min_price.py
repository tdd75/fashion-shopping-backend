# Generated by Django 4.1.6 on 2023-02-12 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_max_price_product_min_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='max_price',
            field=models.DecimalField(decimal_places=2, default=None, editable=False, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='min_price',
            field=models.DecimalField(decimal_places=2, default=None, editable=False, max_digits=12, null=True),
        ),
    ]