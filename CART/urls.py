# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    # Other URL patterns...
    # path('add_to_cart/<int:id>/', add_to_cart, name='some_view'),
    path('add_to_cart/<str:product_variant_id>/', add_variant_to_cart, name='add_to_cart'),
    path('check_variant_in_cart/<str:product_variant_id>/', check_variant_in_cart, name='check_variant_in_cart'),
    path('decrement_cart_item/<str:product_variant_id>/', decrement_cart_item, name='decrement_cart_item'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('get_cart_count/', get_cart_count, name='get_cart_count'),
    path('cart/remove-item/<str:product_variant_id>/', clear_cart_item, name='clear_cart_item'),

]
