from django.urls import path, include

urlpatterns = [
    path('auth/', include('custom_auth.urls')),
    path('users/', include('custom_users.urls')),
    path('addresses/', include('addresses.urls')),
    path('products/', include('products.urls')),
    path('product-variants/', include('product_variants.urls')),
    path('reviews/', include('reviews.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('discount-tickets/', include('discount_tickets.urls')),
    path('chat/', include('chat.urls')),
    path('transactions/', include('transactions.urls')),
    path('analytic/', include('analytic.urls')),
]

handler500 = 'rest_framework.exceptions.server_error'
