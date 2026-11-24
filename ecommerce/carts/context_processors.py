from django.db.models import Sum

from .models import CartItem


def cart_item_count(request):
    session_key = request.session.session_key
    if not session_key:
        return {'cart_item_count': 0}

    count = CartItem.objects.filter(
        cart_id=session_key,
        is_active=True,
    ).aggregate(total=Sum('quantity'))['total'] or 0
    return {'cart_item_count': count}
