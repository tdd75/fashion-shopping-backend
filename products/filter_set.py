from django_filters.rest_framework import filters
from django_filters import FilterSet


class ProductFilterSet(FilterSet):
    stocks = filters.BooleanFilter(method='is_positive_number')

    def is_positive_number(self, queryset, name, value):
        if value == True:
            return queryset.filter(stocks__gt=0)

        return queryset
