from django.urls import path, include


urlpatterns = [
    path('auth/', include('custom_auth.urls')),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('product_types/', include('product_types.urls')),
]
