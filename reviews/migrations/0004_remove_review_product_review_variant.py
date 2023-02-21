# Generated by Django 4.1.6 on 2023-02-08 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("product_variants", "0001_initial"),
        ("reviews", "0003_alter_review_rating"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="review",
            name="product",
        ),
        migrations.AddField(
            model_name="review",
            name="variant",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="product_variants.productvariant",
            ),
            preserve_default=False,
        ),
    ]