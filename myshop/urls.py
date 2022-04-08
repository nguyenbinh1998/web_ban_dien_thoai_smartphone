from django.urls import path
from . import views
urlpatterns = [
    path('store/', views.store, name="store"),
    path('store/<slug:category_slug>/', views.store, name="store_by_category"),
    path('product/<slug:product_slug>/', views.product_detail, name="product_detail"),  
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('remove/<int:product_id>/', views.remove, name="remove"),
]