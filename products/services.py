from .models import Product


def update_favorite(*, product: Product, user_id: int, is_favorite: bool):
    if is_favorite:
        product.favorited_users.add(user_id)
    else:
        product.favorited_users.remove(user_id)
