from django.db import models

from store.models import Product


class Cart(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('cart', 'product'), name='unique_product_per_cart'),
        ]

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.quantity} × {self.product.product_name}'
