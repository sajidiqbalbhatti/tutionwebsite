from django.urls import path
from django.views.generic import TemplateView
from .import views

urlpatterns = [
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('refund-policy/', views.refund_policy, name='refund_policy'),
    path('service-policy/', views.service_policy, name='service_policy'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
    path("data-deletion/", TemplateView.as_view(template_name="pages/data-deletion.html"), name="data_deletion"),

]
