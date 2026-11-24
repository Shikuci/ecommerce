from django.test import TestCase
from django.urls import reverse

from store.models import Category, Product

from .models import CartItem


class CartViewTests(TestCase):
    def setUp(self):
        category = Category.objects.create(category_name='Audio', slug='audio')
        self.product = Product.objects.create(
            product_name='Headphones',
            slug='headphones',
            description='Wireless headphones',
            price=75,
            images='photos/products/headphones.jpg',
            stock=2,
            is_available=True,
            category=category,
        )

    def add_product(self):
        return self.client.post(reverse('add_cart', args=[self.product.pk]))

    def test_cart_starts_empty(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Таны сагс хоосон байна.')

    def test_add_cart_caps_quantity_at_stock(self):
        self.add_product()
        self.add_product()
        self.add_product()
        item = CartItem.objects.get(product=self.product)
        self.assertEqual(item.quantity, self.product.stock)

        response = self.client.get(reverse('cart'))
        self.assertContains(response, '150 ₮')
        self.assertEqual(response.context['quantity'], 2)

    def test_remove_one_and_remove_item(self):
        self.add_product()
        self.add_product()
        self.client.post(reverse('remove_cart', args=[self.product.pk]))
        self.assertEqual(CartItem.objects.get(product=self.product).quantity, 1)
        self.client.post(reverse('remove_cart_item', args=[self.product.pk]))
        self.assertFalse(CartItem.objects.filter(product=self.product).exists())
