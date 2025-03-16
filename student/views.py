from django.shortcuts import get_object_or_404, redirect,render
from django.db import IntegrityError
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator

from users.models import User
from .models import Student
from  courses.models import *
from .forms import StudentForm


@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'student/student_list.html'
    context_object_name = 'students'
    


@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'student/student_detail.html'
    context_object_name = 'student'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()

        # ✅ Ensure courses are passed in context
        context["enrolled_courses"] = student.enrolled_courses.all()  
        return context


@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class StudentCreateView(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student/student_form.html'
    success_url = reverse_lazy('student:student_list')
    
    def form_valid(self, form):
        """Handles valid form submission and prevents duplicate profiles."""
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, "A profile already exists for this user.")
            return redirect('Tutor:tutor-profile-create')

    def form_invalid(self, form):
        messages.error(self.request, "There were errors in your form. Please correct them and try again.")
        return self.render_to_response(self.get_context_data(form=form))
    
    def test_func(self):
        return self.request.user.role == User.STUDENT

    # def handle_no_permission(self):
    #     if not self.request.user.is_authenticated:
    #         return redirect('users:login')
    #     messages.error(self.request, "You don't have permission to access this page.")
    #     return redirect('home_page')
   

@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class StudentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student/student_form.html'
    success_url = reverse_lazy('student:student_list')

    def test_func(self):
        student = self.get_object()
        return self.request.user == student.user

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('users:login')
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('users:login')


@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class StudentView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'student/student_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Check if user is a student
        if user.is_authenticated and hasattr(user, 'student'):
            student = user.student  
            context['courses_enrolled_count'] = student.enrolled_courses.count()  
            context['enrolled_courses'] = student.enrolled_courses.all()  
        else:
            context['courses_enrolled_count'] = 0
            context['enrolled_courses'] = []

        return context  # Ensure you return context
 
        
        

    def test_func(self):
        return hasattr(self.request.user, 'role') and self.request.user.role == User.STUDENT

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('users:login')
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('users:login')
@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')

class StudentProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = "student/student_confirm_delete.html"
    success_url = reverse_lazy("home_page")  # Redirect to home after deletion

    def get_object(self, queryset=None):
        return self.request.user.student  # Delete the logged-in student's profile

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Your profile has been deleted successfully.")
        return super().delete(request, *args, **kwargs)
def search_student(request):
    query = request.GET.get('query', '').strip()
    students = []

    if len(query) >= 3:
        students = Student.objects.filter(user__username__icontains=query)
        if not students:
            message = "No students found."
        else:
            message = None
    else:
        message = "Please enter at least 3 characters to search."

    return render(request, 'student/student_search.html', {
        'students': students,
        'query': query,
        'message': message
    })
    
    





