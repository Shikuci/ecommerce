from django.shortcuts import render, get_object_or_404

from .models import Category, Product


def store(request, cat_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)

    current_category = None

    if cat_slug:
        current_category = get_object_or_404(
            Category,
            slug=cat_slug
        )

        products = products.filter(
            category=current_category
        )

    context = {
        'categories': categories,
        'products': products,
        'current_category': current_category,
    }

    return render(
        request,
        'store/store.html',
        context
    )


def product_detail(request, cat_slug, pro_slug):
    single_product = get_object_or_404(
        Product,
        category__slug=cat_slug,
        slug=pro_slug
    )

    context = {
        'single_product': single_product,
    }

    return render(
        request,
        'store/product_detail.html',
        context
    )