from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from .models import Product
from .serializers import ProductSerializer, ProductFavoriteSerializer
from .filter_set import ProductFilterSet


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
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
        if serializer.data['is_favorite']:
            request.user.favorite_products.add(pk)
        else:
            request.user.favorite_products.remove(pk)
        return Response({'status': 'Update succssfully.'}, status=status.HTTP_200_OK)
