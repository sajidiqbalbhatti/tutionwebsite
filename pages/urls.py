from django.urls import path
from .import views

urlpatterns = [
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('refund-policy/', views.refund_policy, name='refund_policy'),
    path('service-policy/', views.service_policy, name='service_policy'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
]
