from django_filters.rest_framework import filters
from django_filters import FilterSet


class DiscountTicketFilterSet(FilterSet):
    is_saved = filters.BooleanFilter(method='is_saved_ticket')

    def is_saved_ticket(self, queryset, name, value):
        if value == True:
            return queryset.filter(ticketuserrel__user_id=self.request.user.id)
        elif value == False:
            return queryset.exclude(ticketuserrel__user_id=self.request.user.id)
        return queryset
