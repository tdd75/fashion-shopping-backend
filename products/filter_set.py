from django_filters.rest_framework import filters
from django_filters import FilterSet


class ProductFilterSet(FilterSet):
    in_stock = filters.BooleanFilter(method='is_positive_number')
    is_favorite = filters.BooleanFilter(method='is_favorite_product')
    min_price = filters.NumberFilter(field_name='min_price', lookup_expr='gt')
    max_price = filters.NumberFilter(field_name='max_price', lookup_expr='lt')
    color = filters.CharFilter(
        field_name='productvariant__color', lookup_expr='icontains')
    size = filters.CharFilter(
        field_name='productvariant__size', lookup_expr='icontains')
    category_id = filters.NumberFilter(field_name='category__id')

    def is_positive_number(self, queryset, name, value):
        if value == True:
            return queryset.filter(stocks__gt=0)
        return queryset

    def is_favorite_product(self, queryset, name, value):
        if value == True:
            return queryset.filter(favorited_users__id=self.request.user.id)
        elif value == False:
            return queryset.exclude(favorited_users__id=self.request.user.id)
        return queryset
