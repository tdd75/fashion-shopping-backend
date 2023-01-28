from safedelete.managers import SafeDeleteManager, SafeDeleteQueryset


class TransactionQuerySet(SafeDeleteQueryset):
    pass


class TransactionManager(SafeDeleteManager):
    pass
