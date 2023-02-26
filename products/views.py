from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from fashion_shopping_backend.celery import calculate_product_vector
from fashion_shopping_backend.helpers import convert_to_base64
from product_variants.models import ProductVariant
from product_categories.models import ProductCategory
from .models import Product
from .serializers import *
from .filter_set import ProductFilterSet


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.has_price().prefetch_related('productvariant_set')
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_class = ProductFilterSet
    search_fields = ('name', 'description')
    ordering_fields = ('min_price', 'max_price', 'rating', 'created_at')
    ordering = ('id',)

    @action(detail=True, methods=['post'], serializer_class=ProductFavoriteSerializer, url_path='update-favorite')
    def update_favorite(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instace = self.get_object()
        instace.update_is_favorite(
            self.request.user.id, serializer.validated_data['is_favorite'])
        return Response({'message': 'Update succssfully.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], serializer_class=ProductImageSearchSerializer, url_path='search-image')
    def search_by_image(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        results = Product.objects.search_by_image(request.data['image'])
        serialized_data = ProductSerializer(
            results, many=True, context={'request': request}).data
        return Response({'results': serialized_data, 'count': len(serialized_data)}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='related-products')
    def get_related_products(self, request, pk=None):
        instance = self.get_object()
        results = Product.objects.search_by_image(
            convert_to_base64(instance.image), exclude_ids=[instance.id])
        queryset = self.filter_queryset(results)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], serializer_class=ProductFilterSerializer,
            url_path='product-filter')
    def get_filter(self, request):
        serializer = self.get_serializer(data={
            'price_range': Product.objects.get_price_range(),
            'colors': ProductVariant.objects.get_color_list(),
            'sizes': ProductVariant.objects.get_size_list(),
            'categories': ProductCategory.objects.values('id', 'name').distinct('name'),
        })
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductAdminViewSet(viewsets.ModelViewSet):
    serializer_class = ProductAdminSerializer
    queryset = Product.objects.all().prefetch_related('productvariant_set')
    permission_classes = (IsAdminUser,)
    filter_backends = (
        # DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    # filterset_class = ProductFilterSet
    search_fields = ('name', 'description')
    ordering_fields = '__all__'
    ordering = ('id',)

    def create(self, request, *args, **kwargs):
        created_product = super().create(request, *args, **kwargs)
        calculate_product_vector.delay(created_product.id)
        return created_product

    @action(detail=False, methods=['delete'], serializer_class=ProductAdminBulkDeleteSerializer,
            url_path='bulk-delete')
    def bulk_delete(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for product in serializer.validated_data['ids']:
            product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
