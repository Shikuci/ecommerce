from django.urls import path
from . import views

urlpatterns = [
    # Бүх бараа
    path('', views.store, name='store'),

    # Ангиллаар бараа харах
    path(
        '<slug:cat_slug>/',
        views.store,
        name='products_by_category'
    ),

    # Барааны дэлгэрэнгүй хуудас
    path(
        '<slug:cat_slug>/<slug:pro_slug>/',
        views.product_detail,
        name='product_detail'
    ),
]