from .models import Address


def set_default(*, address: Address, user_id: int):
    Address.objects.filter(
        owner_id=user_id, is_default=True).update(is_default=False)
    address.is_default = True
    address.save()
