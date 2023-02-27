from django_filters.rest_framework import filters
from django_filters import FilterSet


class CartFilterSet(FilterSet):
    updated_at = filters.DateTimeFilter(lookup_expr='gte')
