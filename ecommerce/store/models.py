from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(
        upload_to='photos/categories',
        blank=True
    )

    def __str__(self):
        return self.category_name

    def get_url(self):
        return reverse(
            'products_by_category',
            args=[self.slug]
        )


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse(
            'product_detail',
            args=[self.category.slug, self.slug]
        )


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='gallery',
        verbose_name='Бүтээгдэхүүн',
    )
    image = models.ImageField(
        upload_to='photos/products/gallery',
        verbose_name='Зураг',
    )
    alt_text = models.CharField(max_length=200, blank=True, verbose_name='Зургийн тайлбар')
    order = models.PositiveIntegerField(default=0, verbose_name='Дараалал')

    class Meta:
        ordering = ('order', 'pk')
        verbose_name = 'Бүтээгдэхүүний зураг'
        verbose_name_plural = 'Бүтээгдэхүүний зургууд'

    def __str__(self):
        return f'{self.product.product_name} - зураг {self.order + 1}'
