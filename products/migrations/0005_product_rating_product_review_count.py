# Generated by Django 4.1.6 on 2023-02-12 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_max_price_alter_product_min_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0, editable=False, max_digits=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='review_count',
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=False,
        ),
    ]
