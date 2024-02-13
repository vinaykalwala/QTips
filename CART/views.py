from django.shortcuts import render,redirect
from Ecommerceapp.models import *
from .models import *
from django.http import JsonResponse,HttpResponse


# Create your views here.
from django.shortcuts import get_object_or_404

def add_variant_to_cart(request, product_variant_id, quantity=1):
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

    response_data = {'status': 'success' if success else 'error', 'cart_count': cart.cart_items.count()}
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
    # return JsonResponse(response_data)
    return redirect('/cart/cart-detail/')

def clear_cart(request):
    user = request.user
    cart = User_Cart.objects.get(user=user)
    cart.cart_items.all().delete()

    response_data = {'status': 'success'}
    # return JsonResponse(response_data)

    return redirect('/cart/cart-detail/')

def clear_cart_item(request, product_variant_id):
    user = request.user
    variant = get_object_or_404(Variants, id=product_variant_id)
    print("HIii---------------------------")

    try:
        cart = User_Cart.objects.get(user=user)
        cart_item = CartItem.objects.get(cart=cart, variant=variant)
        cart_item.delete()

        response_data = {'status': 'success'}
    except CartItem.DoesNotExist:
        response_data = {'status': 'error', 'message': 'Item not found in the cart'}

    # return JsonResponse(response_data)

    return redirect('/cart/cart-detail/')


def check_variant_in_cart(request, product_variant_id):
    user = request.user
    variant = get_object_or_404(Variants, id=product_variant_id)

    # Check if the variant is in the user's cart
    in_cart = CartItem.objects.filter(cart__user=user, variant=variant).exists()

    response_data = {'in_cart': in_cart}
    return JsonResponse(response_data)

def get_cart_count(request):
    cart = User_Cart(request)
    cart_count = len(cart.cart)
    return JsonResponse({'cart_count': cart_count})