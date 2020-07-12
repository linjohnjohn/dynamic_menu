from django.urls import path
from . import views
from . import stripe

urlpatterns = [
    path('update_cart/', views.update_cart, name='update_cart'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout_success/', views.checkout_success, name='checkout_success'),
    path('', views.menu, name='home'),

    path('webhook/', stripe.webhook)
]