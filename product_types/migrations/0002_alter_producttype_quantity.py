# Generated by Django 4.1.4 on 2022-12-24 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_types', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producttype',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]