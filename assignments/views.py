from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.core.exceptions import PermissionDenied

from .forms import AssignmentForm, AssignmentSubmissionForm, GradeAssignmentForm
from .models import Assignment, AssignmentSubmission


# ================== LIST ASSIGNMENTS ==================
class AssignmentListView(LoginRequiredMixin, ListView):
    model = Assignment
    template_name = "assignments/assignment_list.html"
    context_object_name = "assignments"
    paginate_by=6

    def get_queryset(self):
        # ✅ Prevent N+1 problem for course & tutor.user
        return Assignment.objects.select_related("course", "tutor__user")


# ================== ASSIGNMENT DETAILS ==================
class AssignmentDetailView(LoginRequiredMixin, DetailView):
    model = Assignment
    template_name = "assignments/assignment_detail.html"
    context_object_name = "assignment"

    def get_queryset(self):
        # ✅ Optimize related objects
        return Assignment.objects.select_related("course", "tutor__user").prefetch_related(
            "submissions__student__user"
        )


# ================== CREATE ASSIGNMENT ==================
@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name="dispatch")
class AssignmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = "assignments/assignment_form.html"
    success_url = reverse_lazy("assignments:assignment_list")

    def test_func(self):
        return hasattr(self.request.user, "tutorprofile")

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to create assignments.")
        return redirect("users:login")
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        course = form.instance.course

        if self.request.user.tutorprofile not in course.tutors.all():
            messages.error(self.request, "You can only create assignments for courses you are a tutor of.")
            return redirect("assignments:assignment_list")

        form.instance.tutor = self.request.user.tutorprofile
        return super().form_valid(form)


# ================== UPDATE ASSIGNMENT ==================
class AssignmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = "assignments/assignment_form.html"
    success_url = reverse_lazy("assignments:assignment_list")

    def test_func(self):
        assignment = self.get_object()
        return self.request.user.tutorprofile == assignment.tutor

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to edit this assignment.")
        return redirect("assignments:assignment_list")

    def form_valid(self, form):
        assignment = self.get_object()
        course = form.cleaned_data['course']

        if self.request.user.tutorprofile not in course.tutors.all():
            messages.error(self.request, "You can only update assignments for your own courses.")
            return redirect("assignments:assignment_list")

        form.instance.tutor = self.request.user.tutorprofile
        messages.success(self.request, "Assignment updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Update failed! Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))


# ================== SEARCH ASSIGNMENT ==================
def assignment_tutor(request):
    query = request.GET.get('query', '').strip()
    assignments = Assignment.objects.none()

    if query and len(query) >= 3:
        assignments = Assignment.objects.filter(
            Q(title__icontains=query) |
            Q(tutor__name__icontains=query) |
            Q(course__title__icontains=query)
        ).select_related("course", "tutor__user").distinct()

    return render(request, 'assignments/search_assignments.html', {
        'assignments': assignments,
        'query': query
    })


# ================== SUBMIT ASSIGNMENT ==================
@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name="dispatch")
class AssignmentSubmissionCreateView(LoginRequiredMixin, CreateView):
    model = AssignmentSubmission
    template_name = "assignments/submission_form.html"
    form_class = AssignmentSubmissionForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in before submitting an assignment.")
            return redirect("users:login")

        assignment = get_object_or_404(Assignment.objects.select_related("course"), id=self.kwargs["assignment_id"])
        course = assignment.course
        is_enrolled = request.user.student.enrolled_courses.filter(id=course.id).exists()

        if not is_enrolled:
            messages.warning(request, "You must be enrolled in the course to submit an assignment.")
            return redirect("assignments:assignment_list")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        student = self.request.user.student
        assignment_id = self.kwargs["assignment_id"]

        if AssignmentSubmission.objects.filter(student=student, assignment_id=assignment_id).exists():
            messages.error(self.request, "You have already submitted this assignment.")
            return redirect("assignments:assignment_list")

        form.instance.student = student
        form.instance.assignment_id = assignment_id
        messages.success(self.request, "Assignment successfully submitted!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error submitting assignment. Please try again.")
        return self.render_to_response(self.get_context_data(form=form))
        
    def get_success_url(self):
        return reverse_lazy("assignments:tutor_submissions")


# ================== DELETE ASSIGNMENT ==================
class AssignmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Assignment
    template_name = "assignments/assignment_delete.html"
    success_url = reverse_lazy("assignments:assignment_list")


# ================== TUTOR VIEW SUBMISSIONS ==================
class TutorAssignmentSubmissionsView(LoginRequiredMixin, ListView):
    model = AssignmentSubmission
    template_name = "submission/tutor_submissions.html"
    context_object_name = "submissions"

    def get_queryset(self):
        return AssignmentSubmission.objects.select_related(
            "assignment__course", "assignment__tutor__user", "student__user"
        )


# ================== SUBMISSION DETAILS ==================
class AssignmentSubmissionDetailView(LoginRequiredMixin, DetailView):
    model = AssignmentSubmission
    template_name = "submission/submission_detail.html"
    context_object_name = "submission"

    def get_queryset(self):
        return AssignmentSubmission.objects.select_related(
            "assignment__course", "assignment__tutor__user", "student__user"
        )


# ================== GRADE ASSIGNMENT ==================
class GradeAssignmentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AssignmentSubmission
    form_class = GradeAssignmentForm
    template_name = "submission/grade_assignment.html"

    def test_func(self):
        submission = self.get_object()
        return submission.assignment.tutor.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have access this submission.")
        return redirect("assignments:tutor_submissions")  
    
    def get_success_url(self):
        return reverse_lazy("assignments:tutor_submissions")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Assignment graded successfully!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "There was an error grading the assignment. Please check the form.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_queryset(self):
        return AssignmentSubmission.objects.select_related(
            "assignment__course", "assignment__tutor__user", "student__user"
        )


# ================== SEARCH SUBMISSIONS ==================
def submission_list(request):
    search_query = request.GET.get("search", "")
    submissions = AssignmentSubmission.objects.all().select_related(
        "student__user", "assignment__course", "assignment__tutor__user"
    )

    if search_query:
        submissions = submissions.filter(
            Q(student__user__username__icontains=search_query) |
            Q(assignment__title__icontains=search_query) |
            Q(assignment__course__title__icontains=search_query)
        )
    
    context = {"submissions": submissions, "search_query": search_query}
    return render(request, "submission/search_sub.html", context)
