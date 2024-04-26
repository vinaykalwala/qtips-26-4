from django import template
import math
register = template.Library()


@register.simple_tag()
def calculate_pricetag(price, Discount):
    try:
        price = float(price)
        Discount = float(Discount) if Discount else 0
        sellprice = price - (price * Discount / 100)
        return "{:.2f}".format(sellprice)
    except (TypeError, ValueError):
        return price


@register.simple_tag()
def progress_bar(total_quantity,Availability):
    progress_bar = Availability
    progress_bar = Availability * (100/total_quantity)
    return math.floor(progress_bar)

@register.filter(name='group_by')
def group_by(value, key):
    result = {}
    for item in value:
        result.setdefault(item[key], []).append(item)
    return result


@register.filter(name='add_price')
def add_price(value, arg):
    return value + arg