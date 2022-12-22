# Generated by Django 4.1.4 on 2022-12-22 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_customuser_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=64)),
                ('district', models.CharField(max_length=64)),
                ('ward', models.CharField(max_length=64)),
                ('detail', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.address'),
        ),
    ]
