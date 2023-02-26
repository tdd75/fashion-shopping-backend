from django.contrib import admin
from django.forms import ModelForm
from django.core.exceptions import ValidationError

# Register your models here.
from product_variants.models import ProductVariant
from .models import Product


class ProductAdminForm(ModelForm):
    def clean(self):
        producttype_total_forms = int(
            self.data['productvariant_set-TOTAL_FORMS'])
        if not producttype_total_forms or \
            not any((bool(self.data[f'productvariant_set-{i}-color'])
                    and self.data.get(f'productvariant_set-{i}-DELETE') != 'on')
                    for i in range(producttype_total_forms)):
            raise ValidationError('Requires at least one product type.')
        return super().clean()


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rating', 'stocks', 'updated_at')
    inlines = (ProductVariantInline,)
    form = ProductAdminForm
    ordering = ('id',)
    actions = ('set_quantity_zero',)
    search_fields = ('id', 'name', 'description')
    list_filter = ('category',)
    exclude = ('feature_vector',)
    readonly_fields = ('min_price', 'max_price', 'rating',
                       'num_sold', 'stocks', 'favorited_users')
