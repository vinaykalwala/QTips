from django.shortcuts import render,redirect
from Ecommerceapp.models import *
from .models import *
from django.http import JsonResponse,HttpResponse


# Create your views here.
from django.shortcuts import get_object_or_404

def add_variant_to_cart(request, product_variant_id, quantity=1):
    print(request.method)
    user = request.user
    variant = get_object_or_404(Variants, id=product_variant_id)

    cart, created = User_Cart.objects.get_or_create(user=user)
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        variant=variant,
        defaults={'quantity': quantity}
    )

    if not item_created:
        cart_item.quantity += quantity
        cart_item.save()

    success = True

    response_data = {'status': 'success' if success else 'error'}

    return JsonResponse(response_data)

def decrement_cart_item(request, product_variant_id):
    user = request.user
    variant = get_object_or_404(Variants, id=product_variant_id)

    cart = User_Cart.objects.get(user=user)
    cart_item = CartItem.objects.get(cart=cart, variant=variant)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        # Delete the cart item if quantity is 1
        cart_item.delete()

    response_data = {'status': 'success', 'quantity': cart_item.quantity}
    return JsonResponse(response_data)

def clear_cart(request):
    user = request.user
    cart = User_Cart.objects.get(user=user)
    cart.cart_items.all().delete()

    response_data = {'status': 'success'}
    return JsonResponse(response_data)