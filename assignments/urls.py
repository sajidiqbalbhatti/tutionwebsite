from django.urls import path
from .views import AssignmentDeleteView, AssignmentListView, AssignmentDetailView, AssignmentCreateView, AssignmentSubmissionCreateView, AssignmentSubmissionDetailView, AssignmentUpdateView, GradeAssignmentView, TutorAssignmentSubmissionsView, submission_list

app_name = 'assignments'

urlpatterns = [
    path('course/', AssignmentListView.as_view(), name='assignment_list'),

    path('detail/<int:pk>/', AssignmentDetailView.as_view(), name='detail'),
    path('create/', AssignmentCreateView.as_view(), name='create'),
    path('submit/<int:assignment_id>/', AssignmentSubmissionCreateView.as_view(), name='submit'),
    path('<int:pk>/edit/', AssignmentUpdateView.as_view(), name='assignment_edit'),
    path('delete/<int:pk>/', AssignmentDeleteView.as_view(), name='delete'),
    path('submissions/', TutorAssignmentSubmissionsView.as_view(), name='tutor_submissions'),
    path('submissions/<int:pk>/', AssignmentSubmissionDetailView.as_view(), name='submission_detail'),
    path('grade-assignment/<int:pk>/', GradeAssignmentView.as_view(), name='grade_assignment'),
    path('search/',submission_list , name='search_assignment')





]
