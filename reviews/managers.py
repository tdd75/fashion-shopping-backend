from safedelete.managers import SafeDeleteManager, SafeDeleteQueryset


class ReviewQuerySet(SafeDeleteQueryset):
    pass


class ReviewManager(SafeDeleteManager):
    pass
