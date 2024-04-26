from django.shortcuts import render,redirect
from Ecommerceapp.models import *
from .models import *
from django.http import JsonResponse,HttpResponse


# Create your views here.
from django.shortcuts import get_object_or_404
def add_variant_to_cart(request, product_variant_id, quantity=1):
    user = request.user
    variant = get_object_or_404(Variants, id=product_variant_id)

    # Get the product associated with the variant
    product = variant.product

    # Ensure that the variant has a valid price
    if variant.price is None:
        # Handle the case where the variant price is not available
        # You can return an error message or redirect the user
        return JsonResponse({'status': 'error', 'message': 'Variant price is not available'})

    # Get or create the user's cart
    cart, created = User_Cart.objects.get_or_create(user=user)

    # Get or create the cart item for the specified variant
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        variant=variant,
        defaults={
            'quantity': quantity,
            'variant_title': variant.title,
            'variant_price': variant.price,
            'variant_image': variant.image_id,
            'variant_size': variant.size.name,
            'variant_color': variant.color_name,
            'product_id': product.id,
            'packing_cost': product.packing_cost,
            'tax': product.tax,
            'model_name': product.model_name,
            'brand_name': product.brand.Brand_name if product.brand else '',
            'tag_name': product.Tags.name if product.Tags else '',
        }
    )

    # If the cart item already exists, update the quantity
    if not item_created:
        cart_item.quantity += quantity
        cart_item.save()

    # Calculate the total number of items in the cart
    cart_count = cart.cart_items.count()

    # Retrieve the variant price from the cart item
    cart_item_variant_price = cart_item.variant_price

    # Prepare response data
    response_data = {'status': 'success', 'cart_count': cart_count, 'variant_price': cart_item_variant_price}
    return JsonResponse(response_data)





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