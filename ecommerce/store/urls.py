from django.urls import path
from . import views

urlpatterns = [
    # Бүх бараа
    path('stores/', views.store, name='store'),
]