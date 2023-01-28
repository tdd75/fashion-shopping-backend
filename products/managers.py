from safedelete.managers import SafeDeleteManager, SafeDeleteQueryset


class ProductQuerySet(SafeDeleteQueryset):
    pass


class ProductManager(SafeDeleteManager):
    pass
