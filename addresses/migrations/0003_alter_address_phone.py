# Generated by Django 4.1.7 on 2023-02-15 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='phone',
            field=models.CharField(default='0123456789', max_length=20),
            preserve_default=False,
        ),
    ]
