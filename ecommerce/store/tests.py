from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class StoreViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            category_name='Electronics',
            slug='electronics',
        )
        self.products = []
        for number in range(1, 22):
            self.products.append(Product.objects.create(
                product_name=f'Product {number}',
                slug=f'product-{number}',
                description='Sample product',
                price=number * 10,
                images='photos/products/sample.jpg',
                stock=3,
                is_available=True,
                category=self.category,
            ))

    def test_product_and_category_url_helpers(self):
        product = self.products[0]
        self.assertEqual(self.category.get_url(), '/store/category/electronics/')
        self.assertEqual(product.get_url(), '/store/electronics/product-1/')

    def test_product_detail_shows_stock_and_add_button(self):
        response = self.client.get('/store/electronics/product-1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Үлдэгдэл:')
        self.assertContains(response, reverse('add_cart', args=[self.products[0].pk]))

    def test_out_of_stock_product_has_no_add_button(self):
        product = self.products[0]
        product.stock = 0
        product.save(update_fields=['stock'])
        response = self.client.get(product.get_url())
        self.assertContains(response, 'Бараа дууссан')
        self.assertNotContains(response, reverse('add_cart', args=[product.pk]))

    def test_homepage_uses_database_products_and_product_urls(self):
        product = self.products[-1]
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, product.product_name)
        self.assertContains(response, product.get_url())

    def test_store_paginates_and_links_to_products(self):
        response = self.client.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 10)
        self.assertTrue(response.context['page_obj'].has_next())
        self.assertContains(response, '?page=2')

    def test_page_size_can_be_changed_to_twenty(self):
        response = self.client.get(reverse('store'), {'per_page': '20'})
        self.assertEqual(response.context['per_page'], 20)
        self.assertEqual(len(response.context['products']), 20)
        self.assertTrue(response.context['page_obj'].has_next())

    def test_search_matches_product_price_and_displays_empty_result(self):
        response = self.client.get(reverse('search_result'), {'keyword': '30'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Search result')
        self.assertContains(response, 'Product 3')
        self.assertNotContains(response, 'Product 4')

        response = self.client.get(reverse('search_result'), {'keyword': 'no-such-product'})
        self.assertContains(response, 'Хайлтад тохирох үр дүн олдсонгүй.')

    def test_price_range_filters_products(self):
        response = self.client.get(reverse('store'), {'min_price': '30', 'max_price': '50'})
        self.assertEqual(response.context['result_count'], 3)
