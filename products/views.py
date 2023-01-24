from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import Product
from .serializers import *
from .filter_set import ProductFilterSet
from . import services


@extend_schema_view(list=extend_schema(auth=[]), retrieve=extend_schema(auth=[]))
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_class = ProductFilterSet
    search_fields = ('name', 'description')
    ordering_fields = ('price', 'rating')
    ordering = ('id',)

    @action(detail=True, methods=['post'], serializer_class=ProductFavoriteSerializer, url_path='update-favorite')
    def update_favorite(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.update_favorite(**serializer.data,
                                 product=self.get_object(), user_id=request.user.idd)
        return Response({'message': 'Update succssfully.'}, status=status.HTTP_200_OK)
