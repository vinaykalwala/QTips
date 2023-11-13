# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    # Other URL patterns...
    # path('add_to_cart/<int:id>/', add_to_cart, name='some_view'),
    path('add_to_cart/<str:product_variant_id>/', add_variant_to_cart, name='add_to_cart'),
    path('decrement_cart_item/<int:product_variant_id>/', decrement_cart_item, name='decrement_cart_item'),
    path('clear_cart/', clear_cart, name='clear_cart'),

]
