from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from .views import search_tutors, TutorView , TutorProfileCreateView, TutorProfileUpdateView, TutorProfileDetailView, TutorProfileListView, TutorProfileDeleteView


app_name = 'Tutor'

urlpatterns = [

    
    
    path('search/', search_tutors, name='product_search'),

    path('tutor_dashboard/', TutorView.as_view(), name='tutor_dashboard'),
    path('profile/create/', TutorProfileCreateView.as_view(), name='tutor-profile-create'),
    path('profile/update/<int:pk>', TutorProfileUpdateView.as_view(), name='tutor-profile-update'),
    path('profile/<int:pk>/', TutorProfileDetailView.as_view(), name='tutor-profile-detail'),
    path('profiles/', TutorProfileListView.as_view(), name='tutor-profile-list'),
    path('profile/delete/<int:pk>', TutorProfileDeleteView.as_view(), name='tutor-profile-delete'),
   
]
