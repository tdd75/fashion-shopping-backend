# Generated by Django 4.1.7 on 2023-02-26 11:25

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
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=64)),
                ('district', models.CharField(max_length=64)),
                ('ward', models.CharField(max_length=64)),
                ('detail', models.CharField(max_length=255)),
                ('is_default', models.BooleanField()),
            ],
        ),
    ]
