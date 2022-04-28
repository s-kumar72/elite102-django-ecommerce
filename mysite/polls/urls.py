from django.urls import path
from . import views


# empty string signifies home page
urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('charge/', views.charge, name="charge"),
    path('success/', views.successMsg, name="success"),

    path('update_item/', views.updateItem, name="update_item"),
]
