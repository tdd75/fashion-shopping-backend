from safedelete.managers import SafeDeleteManager, SafeDeleteQueryset


class AddressQuerySet(SafeDeleteQueryset):
    pass


class AddressManager(SafeDeleteManager):
    pass
