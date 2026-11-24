from django.urls import path
from . import views

urlpatterns = [
    path('store/', views.store, name='store'),
    path('stores/', views.store, name='store_catalog'),
    path('store/category/<slug:cat_slug>/', views.products_by_category, name='products_by_category'),
    path('store/<slug:cat_slug>/<slug:pro_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search_result, name='search_result'),
]
