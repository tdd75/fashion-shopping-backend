from safedelete.managers import SafeDeleteManager, SafeDeleteQueryset


class ProductTypeQuerySet(SafeDeleteQueryset):
    pass


class ProductTypeManager(SafeDeleteManager):
    pass
