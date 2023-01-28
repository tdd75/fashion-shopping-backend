from safedelete.managers import SafeDeleteManager, SafeDeleteQueryset


class ChatQuerySet(SafeDeleteQueryset):
    pass


class ChatManager(SafeDeleteManager):
    pass