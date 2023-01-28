from safedelete.managers import SafeDeleteManager, SafeDeleteQueryset


class DiscountTicketQuerySet(SafeDeleteQueryset):
    pass


class DiscountTicketManager(SafeDeleteManager):
    pass
