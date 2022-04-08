from django.shortcuts import redirect, render, get_object_or_404
from .models import Category, Customer, Product, OrderItem
from .forms import OrderForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count

def store(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.all()
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = category.products.all()
    

    customers = Customer.objects.annotate(total_order=Count('orders')).order_by('-total_order')[:]
    for customer in customers:
        print(customer.orders.count())
    
    return render(request, 'myshop/store.html', {'category':category, 'categories':categories, 'products':products})



def product_detail(request, product_slug):
    if request.user.is_authenticated:
        customer = request.user.customer
        if request.method == "POST":
            id = request.POST['product_id']
            cart = request.session.get('cart')
            if cart:
                quantity = cart.get(id)
                if quantity:
                    cart[id] += 1
                else:
                    cart[id] = 1
            else:
                cart = {}
                cart[id] = 1
            request.session['cart'] = cart
        product = Product.objects.get(slug=product_slug)
        return render(request, 'myshop/product_detail.html', {'product':product})
    else:
        pass

@login_required
def cart(request):
    cart = request.session.get('cart')
    if cart:
        keys = cart.keys()
        products = Product.objects.filter(id__in=keys)
    else:
        products = []
    return render(request, 'myshop/cart.html', {'products':products})

def get_total_price(request):
    total = 0
    cart = request.session.get('cart')
    try:
        keys = cart.keys()
        products = Product.objects.filter(id__in=keys)
        for product in products:
            id = str(product.id)
            if id in keys:
                total += cart[id] * product.price
        return total
    except:
        return total

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        total_price = get_total_price(request)
        cart = request.session.get('cart')
        try:
            keys = cart.keys()
            if keys:
                products = Product.objects.filter(id__in=keys)
                if customer.can_purchase(total_price):
                    if request.method == "POST":
                        form = OrderForm(request.POST)
                        if form.is_valid():
                            order = form.save()
                            for product in products:
                                OrderItem.objects.create(customer=customer, order=order, product=product, price=product.price, quantity=cart[str(product.id)])
                            customer.budget -= total_price
                            customer.save()
                            request.session['cart'] = {}
                            return render(request, 'myshop/ordered.html', {'order':order})
                    form = OrderForm()
                    return render(request, 'myshop/checkout.html', {'products':products, 'form':form})
                else:
                    messages.warning(request, "You don't enough money to pay this order !!!")
                    return redirect('cart')
            else:
                messages.warning(request, "You have not purchased any items, please purchase before proceeding to checkout!!!")
                return redirect('store')
        except:
            messages.warning(request, "You have not purchased any items, please purchase before proceeding to checkout!!!")
            return redirect('store')
    else:
        pass


def remove(request, product_id):
    id = str(product_id)
    cart = request.session.get('cart')
    if id in cart:
        del cart[id]
    request.session['cart'] = cart
    print(cart.keys())
    return redirect('cart') 