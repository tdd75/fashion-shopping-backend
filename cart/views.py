from rest_framework import mixins, viewsets, filters

from .models import CartItem
from .serializers import CartItemSerializer


class CartItemListCreateUpdateDestroyViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                                             mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                                             viewsets.GenericViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    filter_backends = (
        filters.OrderingFilter,
    )
    ordering = ('-created_at',)

    def get_queryset(self):
        return CartItem.objects.has_owned(self.request.user.id).is_ordered(False).\
            select_related('product_variant')

    def perform_create(self, serializer):
        data = serializer.validated_data
        existed_cart_item = self.get_queryset().by_product_variant_id(
            data['product_variant'].id)
        # update quantity if product type already exists in the cart
        if existed_cart_item:
            serializer.instance = existed_cart_item
            serializer.validated_data['quantity'] = \
                min(existed_cart_item.product_variant.stocks,
                    data['quantity'] + existed_cart_item.quantity)
        return super().perform_create(serializer)
