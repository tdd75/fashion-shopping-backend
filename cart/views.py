from rest_framework import mixins, viewsets

from .models import CartItem
from .serializers import CartItemSerializer


class CartItemListCreateUpdateDestroyViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                                             mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                                             viewsets.GenericViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.has_owned(self.request.user.id).is_ordered().\
            select_related('product_type')

    def perform_create(self, serializer):
        data = serializer.validated_data
        existed_cart_item = self.get_queryset().get_by_product_type_id(
            data['product_type'].id)
        # update quantity if product type already exists in the cart
        if existed_cart_item:
            serializer.instance = existed_cart_item
            serializer.validated_data['quantity'] = \
                min(existed_cart_item.product_type.stocks,
                    data['quantity'] + existed_cart_item.quantity)
        return super().perform_create(serializer)
