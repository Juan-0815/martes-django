from django.urls import path
from . import views

urlpatterns = [
    # Deja vacío para la URL base
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('pago/', views.paypal_payment_view, name='paypal_payment'),
    path('boleta/', views.boleta_view, name='boleta'),  # URL para la boleta
    path('boleta/pdf/', views.boleta_pdf, name='boleta_pdf'),
    path('pago/', views.paypal_payment_view, name='paypal_payment'),  # URL para el pago
]
