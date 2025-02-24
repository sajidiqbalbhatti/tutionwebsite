from django.urls import path
from .views import AssignmentDeleteView, AssignmentListView, AssignmentDetailView, AssignmentCreateView, AssignmentSubmissionCreateView, AssignmentUpdateView

app_name = 'assignments'

urlpatterns = [
    path('course/', AssignmentListView.as_view(), name='assignment_list'),

    path('detail/<int:pk>/', AssignmentDetailView.as_view(), name='detail'),
    path('create/', AssignmentCreateView.as_view(), name='create'),
    path('submit/<int:assignment_id>/', AssignmentSubmissionCreateView.as_view(), name='submit'),
    path('<int:pk>/edit/', AssignmentUpdateView.as_view(), name='assignment_edit'),
    path('delete/<int:pk>/', AssignmentDeleteView.as_view(), name='delete'),


]
