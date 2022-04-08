from django import template
from ..models import Product

register = template.Library()

@register.simple_tag
def get_quantity(product, cart):
    keys = cart.keys()  
    id = str(product.id)
    if id in keys:
        return cart[id]
    return 0

@register.simple_tag
def get_price(product, cart):
    keys = cart.keys()
    id = str(product.id)
    if id in keys:
        price = cart[id] * product.price
        return "{:,}".format(price)
    return 0

@register.simple_tag
def get_total_price(products, cart):
    total = 0
    try:
        keys = cart.keys()
        for product in products:
            id = str(product.id)
            if id in keys:
                total += cart[id] * product.price
        return '{:,}'.format(total)
    except:
        return total