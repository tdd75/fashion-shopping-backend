# Generated by Django 4.1.5 on 2023-01-21 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=128)),
                ('phone', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('city', models.CharField(max_length=64)),
                ('district', models.CharField(max_length=64)),
                ('ward', models.CharField(max_length=64)),
                ('street', models.CharField(max_length=64)),
                ('detail', models.CharField(max_length=255)),
            ],
        ),
    ]
