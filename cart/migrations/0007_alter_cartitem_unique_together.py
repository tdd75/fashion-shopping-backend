# Generated by Django 4.1.5 on 2023-01-26 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together=set(),
        ),
    ]