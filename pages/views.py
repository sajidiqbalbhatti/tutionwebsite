from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def privacy_policy(request):
    return render(request, 'pages/privacy_policy.html')

def refund_policy(request):
    return render(request, 'pages/refund_policy.html')

def service_policy(request):
    return render(request, 'pages/service_policy.html')

def terms_conditions(request):
    return render(request, 'pages/terms_conditions.html')
