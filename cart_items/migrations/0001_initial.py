# Generated by Django 4.1.4 on 2023-01-02 05:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '__first__'),
        ('product_types', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('size', models.CharField(max_length=16)),
                ('color', models.CharField(max_length=32)),
                ('image', models.URLField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('order', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product_types.producttype')),
            ],
        ),
        migrations.AddIndex(
            model_name='cartitem',
            index=models.Index(fields=['order'], name='cart_items__order_i_cd8be6_idx'),
        ),
    ]
