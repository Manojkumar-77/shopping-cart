from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required

def product_list(request):
    categories = Category.objects.all()
    return render(request, "main.html", {"categories": categories})

def aboutus(request):
    return render(request, "aboutus.html")

def contactus(request):
    return render(request, "contactus.html")

def categories(request):
    categories = Category.objects.filter(status=False)
    return render(request, "categories.html", {"categories": categories})

def products(request, category_id=None):
    if category_id is not None:
        category = get_object_or_404(Category, id=category_id, status=False)
        products = Product.objects.filter(category=category, status=False)

    # show all products
    products = Product.objects.filter(status=False).order_by('-created_at')
    return render(request, "products.html", {"products": products})

def all_products(request):
    category_id = request.GET.get('category')
    products = Product.objects.all().order_by('-created_at')
    if category_id:
        products = products.filter(category_id=category_id)
    return render(request, "products.html", {"products": products})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart_view')


@login_required
def increase_quantity(request, item_id):
    """Increase CartItem.quantity by 1 and redirect back to cart."""
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('cart_view')


@login_required
def decrease_quantity(request, item_id):
    """Decrease CartItem.quantity by 1; delete if it reaches zero.

    Redirect back to the cart view afterwards.
    """
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart_view')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('cart_view')
    total = sum(item.subtotal() for item in cart_items)
    if request.method == "POST":
        # Create an Order and corresponding OrderItem rows from the user's cart
        order = Order.objects.create()
        for ci in cart_items:
            OrderItem.objects.create(order=order, product=ci.product, quantity=ci.quantity)

        # Clear the cart after creating the order
        cart_items.delete()
        return render(request, 'checkout_success.html', {'total': total, 'order': order})
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})