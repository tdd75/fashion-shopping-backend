from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import Address
from .serializers import AddressSerializer
from .swagger import ADDRESS_EXAMPLES


@extend_schema_view(create=extend_schema(examples=ADDRESS_EXAMPLES))
class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_fields = ('is_default',)
    ordering = ('-is_default', 'id')

    def get_queryset(self):
        return Address.objects.has_owned(self.request.user.id)
