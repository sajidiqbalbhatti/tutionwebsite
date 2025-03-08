from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView 
from .views import StudentProfileDeleteView, search_student, StudentView, StudentListView, StudentDetailView, StudentCreateView, StudentUpdateView,EnrollInCourseView


app_name = 'student'

urlpatterns = [
    path('search/', search_student, name='student_search'),
    path('course/<int:course_id>/enroll/', EnrollInCourseView.as_view(), name='enroll_course'),

    path('student_dashboard/', StudentView.as_view(), name='student_dashboard'),
    #    path('register/', StudentRegisterView.as_view(), name='student_register'),
    path('', StudentListView.as_view(), name='student_list'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('create/', StudentCreateView.as_view(), name='student_create'),
    path('student/delete/', StudentProfileDeleteView.as_view(), name='student-delete'),

    path('<int:pk>/update/', StudentUpdateView.as_view(), name='student_update'),
]
