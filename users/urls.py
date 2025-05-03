from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from .views import (
    RoleBasedLoginView,
    AdminView,
    ParentView,
    UserSignupView,
)

app_name = 'users'

urlpatterns = [
    path('', AdminView.as_view(), name='admin_dashboard'),
    
    
    path('parent_dashboard/', ParentView.as_view(), name='parent_dashboard'),
    path('forbidden/', TemplateView.as_view(template_name='users/forbidden.html'), name='forbidden'),
    path('logout/', LogoutView.as_view(next_page='home_page'), name='logout'),

    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', RoleBasedLoginView.as_view(template_name='users/login.html'), name='login'),
]
