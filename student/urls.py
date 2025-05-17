from django.urls import path
from .views import StudentProfileDeleteView, search_student, StudentView, StudentListView, StudentDetailView, StudentCreateView, StudentUpdateView


app_name = 'student'

urlpatterns = [
    path('search/', search_student, name='student_search'),
    path('student_dashboard/', StudentView.as_view(), name='student_dashboard'),
    path('', StudentListView.as_view(), name='student_list'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('create/', StudentCreateView.as_view(), name='student_create'),
    path('student/delete/', StudentProfileDeleteView.as_view(), name='student-delete'),
    path('<int:pk>/update/', StudentUpdateView.as_view(), name='student_update'),
]
