from django import template
from CART.models import *

register = template.Library()

@register.simple_tag(takes_context=True)
def calculate_variant_total(context, variant_id):
    user = context['request'].user
    cart_items = CartItem.objects.filter(cart__user=user, variant__id=variant_id)

    total = 0
    for item in cart_items:
        total += item.quantity * item.variant_price

    print(f"Variant ID: {variant_id}, Total: {total}")  # Add this line for debugging
    return total
