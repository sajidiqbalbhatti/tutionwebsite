from django.shortcuts import get_object_or_404, redirect,render
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView
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


@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student/student_form.html'
    success_url = reverse_lazy('student:student_list')

    def form_valid(self, form):
        # Assign the currently logged-in user to the student instance
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # Ensure the logged-in user matches the student instance's user
        student = self.get_object()
        return self.request.user == student.user

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect unauthenticated users to the login page
            return redirect('users:login')
        # Show a permission error message and redirect to the student list
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('home_page')

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

        # Count courses the user is enrolled in
        if user.is_authenticated and hasattr(user, 'student'):
            context['courses_enrolled_count'] = user.student.enrolled_courses.count()
            context['enrolled_courses'] = user.student.enrolled_courses.all()  # List of enrolled courses
        else:
            context['courses_enrolled_count'] = 0
            context['enrolled_courses'] = [] 
        
        return context

    def test_func(self):
        return hasattr(self.request.user, 'role') and self.request.user.role == User.STUDENT

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('users:login')
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('users:login')


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
    
    
class EnrollInCourseView(LoginRequiredMixin, View):
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        if request.user.role == 'student':
            # Check if the student is already enrolled
            if course.students.filter(id=request.user.id).exists():  # Assuming 'students' is a related field in Course
                messages.warning(request, f"You are already enrolled in {course.title}.")
            else:
                course.enroll_student(request.user)
                messages.success(request, f"You have successfully enrolled in {course.title}")
        else:
            messages.error(request, "Only students can enroll in courses.")

        return redirect('courses:course_detail', pk=course.id)




