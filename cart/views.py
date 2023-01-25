from rest_framework import mixins, viewsets

from .models import CartItem
from .serializers import CartItemSerializer


class CartItemListCreateUpdateDestroyViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                                             mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                                             viewsets.GenericViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(owner_id=self.request.user.id)
