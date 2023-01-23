from django.urls import path, include

urlpatterns = [
    path('auth/', include('custom_auth.urls')),
    path('users/', include('users.urls')),
    path('addresses/', include('addresses.urls')),
    path('products/', include('products.urls')),
    path('product-types/', include('product_types.urls')),
    path('reviews/', include('reviews.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('discount-tickets/', include('discount_tickets.urls')),
    path('chat/', include('chat.urls')),
]

handler500 = 'rest_framework.exceptions.server_error'
