from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter
def mnt(value):
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        amount = Decimal('0')
    return f'{amount:,.0f} ₮'
