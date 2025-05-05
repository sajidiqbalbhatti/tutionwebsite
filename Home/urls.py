from django.urls import path
from Home.views import EducationHomepage

urlpatterns = [
    path('',EducationHomepage.as_view(), name='home_page'),
]
