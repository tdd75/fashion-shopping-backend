from rest_framework import mixins, viewsets

from .models import CartItem
from .serializers import CartItemSerializer


class CartItemListCreateUpdateDestroyViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                                             mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                                             viewsets.GenericViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(owner_id=self.request.user.id)

    def perform_create(self, serializer):
        existed_cart_item = self.get_queryset().filter(
            product_type_id=serializer.validated_data['product_type'].id).first()
        # update quantity if cart item already exists
        if existed_cart_item:
            serializer.instance = existed_cart_item
            serializer.validated_data['quantity'] = min(existed_cart_item.product_type.stocks,
                                                        serializer.validated_data['quantity'] + existed_cart_item.quantity)
        serializer.save()
