from django.shortcuts import render, get_object_or_404

from .models import Category, Product


def store(request):
    return render(request, 'store/store.html')


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