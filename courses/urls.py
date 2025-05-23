from django.urls import path
from .views import (
    CourseListView, CourseDetailView, CourseCreateView,
    CourseUpdateView, CourseDeleteView,SearchResultsView,EnrollInCourseView
)

app_name='courses'

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('search/', SearchResultsView, name='search_results'),
    path('course/<int:course_id>/enroll/', EnrollInCourseView.as_view(), name='enroll_course'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('<int:pk>/update/', CourseUpdateView.as_view(), name='course_update'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
]
