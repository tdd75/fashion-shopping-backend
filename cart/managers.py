from safedelete.managers import SafeDeleteManager, SafeDeleteQueryset


class CartQuerySet(SafeDeleteQueryset):
    def has_owned(self, user_id):
        return self.filter(owner_id=user_id)

    def is_ordered(self):
        return self.filter(is_ordered=True)

    def get_by_product_type_id(self, id):
        return self.filter(product_type_id=id).first()


class CartManager(SafeDeleteManager):
    pass
