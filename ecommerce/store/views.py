from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .models import Category, Product


PAGE_SIZE_OPTIONS = (10, 20, 30)


def _product_listing(request, *, cat_slug=None, is_search=False):
    products = Product.objects.select_related('category')
    categories = Category.objects.all().order_by('category_name')
    selected_category = None

    if cat_slug:
        selected_category = get_object_or_404(Category, slug=cat_slug)
        products = products.filter(category=selected_category)

    keyword = request.GET.get('keyword', '').strip()
    if is_search and keyword:
        matching = (
            Q(product_name__icontains=keyword)
            | Q(description__icontains=keyword)
            | Q(category__category_name__icontains=keyword)
        )
        if keyword.isdecimal():
            matching |= Q(price=int(keyword))
        products = products.filter(matching)

    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    if min_price.isdecimal():
        products = products.filter(price__gte=int(min_price))
    if max_price.isdecimal():
        products = products.filter(price__lte=int(max_price))

    per_page_value = request.GET.get('per_page', '10')
    per_page = int(per_page_value) if per_page_value.isdecimal() and int(per_page_value) in PAGE_SIZE_OPTIONS else 10
    products = products.order_by('-created_date', '-pk')
    paginator = Paginator(products, per_page)
    page_obj = paginator.get_page(request.GET.get('page'))
    query_params = request.GET.copy()
    query_params.pop('page', None)

    return render(request, 'store/store.html', {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'keyword': keyword,
        'min_price': min_price,
        'max_price': max_price,
        'query_string': query_params.urlencode(),
        'is_search': is_search,
        'result_count': paginator.count,
        'per_page': per_page,
        'page_size_options': PAGE_SIZE_OPTIONS,
    })


def store(request):
    return _product_listing(request)


def products_by_category(request, cat_slug):
    return _product_listing(request, cat_slug=cat_slug)


def search_result(request):
    return _product_listing(request, is_search=True)


def product_detail(request, cat_slug, pro_slug):
    single_product = get_object_or_404(
        Product.objects.prefetch_related('gallery'),
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

