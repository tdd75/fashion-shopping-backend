from django.contrib import admin

from addresses.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'city',
                    'district', 'ward', 'detail')
    search_fields = ('full_name', 'phone', 'city',
                     'district', 'ward', 'detail')
