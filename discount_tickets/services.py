from .models import Address


def add_ticket(*, address: Address, user_id: int):
    Address.objects.filter(
        owner_id=user_id, is_default=True).update(is_default=False)
    address.is_default = True
    address.save()
