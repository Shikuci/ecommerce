from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
    path('product-detail/', views.product_detail, name='product_detail'),
    path('order-complete/', views.order_complete, name='order_complete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search_result, name='search_result'),
    path('place-order/', views.place_order, name='place_order'),
]