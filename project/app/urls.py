from django.urls import path
from .views import *

urlpatterns = [
    path('products',getProducts),
    path('login', login),
    path('logout', logout),
    path('product', createProduct),
    path('product/<int:pk>', changeproduct),
    path('carts', getCarts),
    path('cart/<int:pk>', changecart),
]