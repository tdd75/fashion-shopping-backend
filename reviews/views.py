from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import Review
from .serializers import ReviewSerializer


@extend_schema_view(list=extend_schema(auth=[]))
class ReviewListCreateViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Review.objects.all().select_related('owner')
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(product=serializer.validated_data['variant'].product)