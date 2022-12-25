from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer


class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    filterset_fields = ('stage',)
    search_fields = ('code',)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return super().get_serializer_class()

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class OrderDetailUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'
