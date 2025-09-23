# urls.py

from django.urls import path
from .views import PayFastCheckoutView,CheckoutPageView

urlpatterns = [
    path('checkout-page/', CheckoutPageView.as_view(), name='checkout_page'),

    path('checkout/', PayFastCheckoutView.as_view(), name='payfast_checkout'),
]
