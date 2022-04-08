from .models import Product

def cart(request):
    cart = request.session.get('cart')
    quantity = 0
    total = 0
    if cart:
        keys = cart.keys()
        products = Product.objects.filter(id__in=keys)
        for product in products:
            if str(product.id) in keys:
                total += cart[str(product.id)] * product.price
                quantity += cart[str(product.id)]
    return {'cart': {'get_total_price':total, 'quantity':quantity}}