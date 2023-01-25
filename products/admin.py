from django.contrib import admin
from django.forms import ModelForm
from django.core.exceptions import ValidationError

# Register your models here.
from product_types.models import ProductType
from .models import Product


class ProductAdminForm(ModelForm):
    def clean(self):
        producttype_total_forms = int(self.data['producttype_set-TOTAL_FORMS'])
        if not producttype_total_forms or \
            not any((bool(self.data[f'producttype_set-{i}-color'])
                    and self.data.get(f'producttype_set-{i}-DELETE') != 'on')
                    for i in range(producttype_total_forms)):
            raise ValidationError('Requires at least one product type.')
        return super().clean()


class ProductTypeInline(admin.TabularInline):
    model = ProductType


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rating', 'stocks', 'updated_at')
    inlines = (ProductTypeInline,)
    form = ProductAdminForm
    ordering = ('id',)
    actions = ('set_quantity_zero',)


admin.site.register(Product, ProductAdmin)
