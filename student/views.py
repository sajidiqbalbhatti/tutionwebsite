from django.shortcuts import get_object_or_404, redirect, render
from django.db import IntegrityError
from django.views.generic import (
    TemplateView, CreateView, UpdateView, DetailView, ListView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator
from users.models import User
from .models import Student
from courses.models import *
from .forms import StudentForm
from django.core.cache import cache

CACHE_DECORATOR = method_decorator(
    cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch'
)

@CACHE_DECORATOR
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'student/student_list.html'
    context_object_name = 'students'
    
    def get_queryset(self):
        cache_key = "student_list"
        students = cache.get(cache_key)
        
        if not students:
            print("⚡ Cache MISS - Fetching from DB")  # debug
            students = (
                Student.objects.select_related("user")
                .prefetch_related("enrolled_courses")
                .all()
            )
            cache.set(cache_key,students,300)
        else:
             print("✅ Cache HIT - Using cached data")  # debug
        return students



@CACHE_DECORATOR
class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'student/student_detail.html'
    context_object_name = 'student'
    def get_object(self):
        cache_key = f"student_detail_{self.kwargs['pk']}"
        student = cache.get(cache_key)
        if not student:
            print("⚡ Cache MISS - Fetching from DB")  # debug
            student = (
                Student.objects
                .select_related("user")
                .prefetch_related("enrolled_courses")
                .get(pk=self.kwargs['pk'])
            )
            cache.set(cache_key, student, 10)
        else:
            print("✅ Cache HIT - Using cached data")  # debug
        return student

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enrolled_courses"] = self.get_object().enrolled_courses.all()
        return context

@CACHE_DECORATOR
class StudentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student/student_form.html'
    success_url = reverse_lazy('student:student_list')

    def form_valid(self, form):
        if hasattr(self.request.user, 'student'):  # Check if student profile already exists
             messages.error(self.request, "A profile already exists for this user.")
             return redirect('student:student_list')  # Redirect to student list page

        form.instance.user = self.request.user
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request, "There were errors in your form. Please correct them and try again.")
        return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
       return self.request.user.role.lower() == "student"



@CACHE_DECORATOR
class StudentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student/student_form.html'
    success_url = reverse_lazy('student:student_list')

    def test_func(self):
        return self.request.user == self.get_object().user

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('users:login')
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('users:login')
    def form_valid(self, form):
        response = super().form_valid(form)
        cache_key = f"student_detail_{self.object.pk}"
        cache.delete(cache_key)  # ✅ Cache clear
        print(f"🗑️ Cache deleted after update: {cache_key}")
        return response

@CACHE_DECORATOR
class StudentView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'student/student_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated and hasattr(user, 'student'):
            student = user.student
            context['courses_enrolled_count'] = student.enrolled_courses.count()
            context['enrolled_courses'] = student.enrolled_courses.all()
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

@CACHE_DECORATOR
class StudentProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = "student/student_confirm_delete.html"
    success_url = reverse_lazy("home_page")

    def get_object(self, queryset=None):
        return self.request.user.student

    def delete(self, request, *args, **kwargs):
        # pehle parent class ka delete call karo
        response = super().delete(request, *args, **kwargs)

        # Cache clear karo
        cache.clear()

        # Success message
        messages.success(request, "Your profile has been deleted successfully.")

        return response

from django.db import connection

def search_student(request):
    query = request.GET.get('query', '').strip()
    students = Student.objects.none()

    if query and len(query) >= 3:
        students = Student.objects.filter(
            Q(name__icontains=query) |
            Q(level__icontains=query) |
            Q(enrolled_courses__title__icontains=query)
        ).select_related("user").prefetch_related("enrolled_courses").distinct()

    print("🔥 Queries Run:", len(connection.queries))  # Debug line
    for q in connection.queries:
        print(q["sql"])

    return render(request, 'student/student_search.html', {'students': students, 'query': query})





