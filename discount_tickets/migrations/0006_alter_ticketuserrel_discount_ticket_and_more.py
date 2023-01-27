# Generated by Django 4.1.5 on 2023-01-27 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discount_tickets', '0005_rename_custom_user_ticketuserrel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketuserrel',
            name='discount_ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discount_tickets.discountticket'),
        ),
        migrations.AlterField(
            model_name='ticketuserrel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
