# Generated by Django 4.1.5 on 2023-01-28 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0003_remove_forgotpasswordcode_recover_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='forgotpasswordcode',
            name='deleted',
            field=models.DateTimeField(db_index=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='forgotpasswordcode',
            name='deleted_by_cascade',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
