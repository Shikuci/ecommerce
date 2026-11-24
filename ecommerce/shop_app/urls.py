from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('order-complete/', views.order_complete, name='order_complete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('place-order/', views.place_order, name='place_order'),
]
