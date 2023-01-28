from safedelete.managers import SafeDeleteManager, SafeDeleteQueryset


class OrderQuerySet(SafeDeleteQueryset):
    def has_owned(self, user_id):
        return self.filter(owner_id=user_id)


class OrderManager(SafeDeleteManager):
    def clean_items_in_cart(self):
        pass
