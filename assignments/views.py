from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control

from .forms import AssignmentForm, AssignmentSubmissionForm
from .models import Assignment, AssignmentSubmission

# List all assignments
class AssignmentListView(LoginRequiredMixin, ListView):
    model = Assignment
    template_name = 'assignments/assignment_list.html'
    context_object_name = 'assignments'

# Show details of a specific assignment
class AssignmentDetailView(LoginRequiredMixin, DetailView):
    model = Assignment
    template_name = 'assignments/assignment_detail.html'
    context_object_name = 'assignment'

# Tutor can create a new assignment
@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class AssignmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignments/assignment_form.html'
    success_url = reverse_lazy('assignments:assignment_list')

    def test_func(self):
        """Ensure only authenticated tutors can create assignments"""
        return hasattr(self.request.user, 'tutorprofile')

    def handle_no_permission(self):
        """Redirect unauthorized users to another page with an error message"""
        messages.error(self.request, "You are not authorized to create assignments.")
        return redirect('users:login')

    def form_valid(self, form):
        form.instance.tutor = self.request.user.tutorprofile  
        return super().form_valid(form)

    # def form_invalid(self, form):
    #     messages.error(self.request, "Form submission failed! Please correct the errors below.")
    #     return self.render_to_response(self.get_context_data(form=form))


class AssignmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignments/assignment_form.html'
    success_url = reverse_lazy('assignments:assignment_list')

    def test_func(self):
        """Ensure only the tutor who created the assignment can edit it"""
        assignment = self.get_object()
        return self.request.user.is_authenticated and self.request.user.tutorprofile == assignment.tutor

    def handle_no_permission(self):
        """Redirect unauthorized users"""
        messages.error(self.request, "You are not authorized to edit this assignment.")
        return redirect('assignments:assignment_list')

    def form_valid(self, form):
        messages.success(self.request, "Assignment updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Update failed! Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))
# Students can submit assignments
@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class AssignmentSubmissionCreateView(LoginRequiredMixin, CreateView):
    model = AssignmentSubmission
    template_name = 'assignments/submission_form.html'
    form_class = AssignmentSubmissionForm
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in before submitting an assignment.")
            return redirect('users:login')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.student = self.request.user.student  
        form.instance.assignment_id = self.kwargs['assignment_id']
        messages.success(self.request, "Assignment successfully submitted!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error submitting assignment. Please try again.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('assignments:assignment_list')




class AssignmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Assignment
    template_name = "assignments/assignment_delete.html"
    success_url = reverse_lazy('assignments:assignment_list')  # Redirect after deletion
