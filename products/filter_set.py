from django_filters.rest_framework import filters
from django_filters import FilterSet


class ProductFilterSet(FilterSet):
    in_stock = filters.BooleanFilter(method='is_positive_number')
    is_favorite = filters.BooleanFilter(method='is_favorite_product')
    min_price = filters.NumberFilter(method='min_price_filter')
    max_price = filters.NumberFilter(method='max_price_filter')
    color = filters.CharFilter(
        field_name='productvariant__color', lookup_expr='icontains')
    size = filters.CharFilter(
        field_name='productvariant__size', lookup_expr='icontains')
    category_id = filters.NumberFilter(field_name='category__id')
    category = filters.CharFilter(field_name='category__name')

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

    def min_price_filter(self, queryset, name, value):
        return queryset.with_min_price().filter(annotate_min_price__gt=value)

    def max_price_filter(self, queryset, name, value):
        return queryset.with_max_price().filter(annotate_max_price__lt=value)
