from django.urls import path
from .views import contact_view,feedback_view

app_name ='contact'
urlpatterns = [
    path('', contact_view, name='contact'),
    path('feedback/', feedback_view, name='feedback'),
    
]
