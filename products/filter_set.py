from django_filters.rest_framework import filters
from django_filters import FilterSet


class ProductFilterSet(FilterSet):
    in_stock = filters.BooleanFilter(method='is_positive_number')
    is_favorite = filters.BooleanFilter(method='is_favorite_product')

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
