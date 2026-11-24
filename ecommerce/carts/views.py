from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from store.models import Product

from .models import Cart, CartItem


def _cart_id(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    return session_key


@require_POST
def add_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if not product.is_available or product.stock <= 0:
        messages.warning(request, 'Уучлаарай, энэ бараа дууссан байна.')
        return redirect(product.get_url())

    cart, _ = Cart.objects.get_or_create(id=_cart_id(request))
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 0, 'is_active': True},
    )
    if item.quantity < product.stock:
        item.quantity += 1
        item.is_active = True
        item.save(update_fields=['quantity', 'is_active'])
    else:
        messages.warning(request, 'Сагсан дахь тоо ширхэг барааны үлдэгдлээс хэтэрч болохгүй.')

    return redirect('cart')


@require_POST
def remove_cart(request, product_id):
    session_key = request.session.session_key
    if session_key:
        item = CartItem.objects.filter(
            cart_id=session_key,
            product_id=product_id,
            is_active=True,
        ).first()
        if item:
            if item.quantity > 1:
                item.quantity -= 1
                item.save(update_fields=['quantity'])
            else:
                item.delete()
    return redirect('cart')


@require_POST
def remove_cart_item(request, product_id):
    session_key = request.session.session_key
    if session_key:
        CartItem.objects.filter(
            cart_id=session_key,
            product_id=product_id,
        ).delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    cart_items = []
    session_key = request.session.session_key
    if session_key:
        cart = Cart.objects.filter(pk=session_key).first()
        if cart:
            items = cart.items.filter(is_active=True).select_related('product', 'product__category')
            for item in items:
                if not item.product.is_available or item.product.stock <= 0:
                    item.delete()
                    continue
                if item.quantity > item.product.stock:
                    item.quantity = item.product.stock
                    item.save(update_fields=['quantity'])
                total += item.subtotal
                quantity += item.quantity
                cart_items.append(item)

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'is_empty': not cart_items,
    }
    return render(request, 'cart.html', context)
