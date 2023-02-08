from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from fashion_shopping_backend.celery import calculate_product_vector
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from .models import Product
from .serializers import *
from .filter_set import ProductFilterSet


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().prefetch_related('productvariant_set')
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
        instace = self.get_object()
        instace.update_is_favorite(
            self.request.user.id, serializer.validated_data['is_favorite'])
        return Response({'message': 'Update succssfully.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], serializer_class=ProductImageSearchSerializer, url_path='search-image')
    def search_by_image(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data['image']
        fs = FileSystemStorage(location=settings.BASE_DIR / 'tmp')
        filename = fs.save(image.name, image)
        results = Product.objects.search_by_image('/tmp/' + filename)
        serialized_data = ProductSerializer(
            results, many=True, context={'request': request}).data
        return Response({'results': serialized_data}, status=status.HTTP_200_OK)


class ProductAdminViewSet(viewsets.ModelViewSet):
    serializer_class = ProductAdminSerializer
    queryset = Product.objects.all().prefetch_related('productvariant_set')
    permission_classes = (IsAdminUser,)
    # filter_backends = (
    #     DjangoFilterBackend,
    #     filters.SearchFilter,
    #     filters.OrderingFilter,
    # )
    # filterset_class = ProductFilterSet
    # search_fields = ('name', 'description')
    # ordering_fields = ('price', 'rating')
    # ordering = ('id',)

    def create(self, request, *args, **kwargs):
        created_product = super().create(request, *args, **kwargs)
        calculate_product_vector.delay(created_product.id)
        return created_product
