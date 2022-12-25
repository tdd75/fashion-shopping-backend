from django.urls import path, include


urlpatterns = [
    path('auth/', include('custom_auth.urls')),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('product-types/', include('product_types.urls')),
    path('reviews/', include('reviews.urls')),
    path('cart-items/', include('cart_items.urls')),
    path('orders/', include('orders.urls')),
]
