# ✅ Core Django imports
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import (
    TemplateView, CreateView, UpdateView, DetailView, ListView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.core.cache import cache

# ✅ Local imports
from users.models import User
from .models import Student
from courses.models import Course   # ✅ avoid wildcard import (*)
from .forms import StudentForm


# ==========================
# 🔹 Cache Decorator
# ==========================
CACHE_DECORATOR = method_decorator(
    cache_control(no_cache=True, must_revalidate=True, no_store=True), 
    name='dispatch'
)


# ==========================
# 🔹 Student List View
# ==========================
@CACHE_DECORATOR
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'student/student_list.html'
    context_object_name = 'students'
    
    def get_queryset(self):
        """
        ✅ Optimized to prevent N+1 problem:
        - select_related("user") → avoid extra queries for each student's user
        - prefetch_related("enrolled_courses") → avoid extra queries for enrolled courses
        """
        cache_key = "student_list"
        students = cache.get(cache_key)
        
        if not students:
            print("⚡ Cache MISS - Fetching from DB")
            students = (
                Student.objects
                .select_related("user")
                .prefetch_related("enrolled_courses")
                .all()
            )
            cache.set(cache_key, students, 300)
        else:
            print("✅ Cache HIT - Using cached data")

        return students


# ==========================
# 🔹 Student Detail View
# ==========================
@CACHE_DECORATOR
class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'student/student_detail.html'
    context_object_name = 'student'

    def get_object(self):
        """
        ✅ Optimized: select_related + prefetch_related 
        to prevent N+1 queries in template.
        """
        cache_key = f"student_detail_{self.kwargs['pk']}"
        student = cache.get(cache_key)

        if not student:
            print("⚡ Cache MISS - Fetching from DB")
            student = (
                Student.objects
                .select_related("user")
                .prefetch_related("enrolled_courses")
                .get(pk=self.kwargs['pk'])
            )
            cache.set(cache_key, student, 30)
        else:
            print("✅ Cache HIT - Using cached data")

        return student

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # enrolled_courses already prefetched, so no extra queries
        context["enrolled_courses"] = self.get_object().enrolled_courses.all()
        return context


# ==========================
# 🔹 Student Create View
# ==========================
@CACHE_DECORATOR
class StudentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student/student_form.html'
    success_url = reverse_lazy('student:student_list')

    def form_valid(self, form):
        # Prevent duplicate student profile for the same user
        if hasattr(self.request.user, 'student'):
            messages.error(self.request, "A profile already exists for this user.")
            return redirect('student:student_list')

        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There were errors in your form. Please correct them and try again."
        )
        return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        return self.request.user.role.lower() == "student"


# ==========================
# 🔹 Student Update View
# ==========================
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


# ==========================
# 🔹 Student Dashboard View
# ==========================
@CACHE_DECORATOR
class StudentView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'student/student_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated and hasattr(user, 'student'):
            # ✅ Optimized: courses are prefetched automatically
            student = (
                Student.objects
                .select_related("user")
                .prefetch_related("enrolled_courses")
                .get(pk=user.student.pk)
            )
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


# ==========================
# 🔹 Student Profile Delete View
# ==========================
@CACHE_DECORATOR
class StudentProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = "student/student_confirm_delete.html"
    success_url = reverse_lazy("home_page")

    def get_object(self, queryset=None):
        return self.request.user.student


# ==========================
# 🔹 Search Student View
# ==========================
def search_student(request):
    query = request.GET.get('query', '').strip()
    students = Student.objects.none()

    if query and len(query) >= 3:
        students = (
            Student.objects.filter(
                Q(name__icontains=query) |
                Q(level__icontains=query) |
                Q(enrolled_courses__title__icontains=query)
            )
            .select_related("user")
            .prefetch_related("enrolled_courses")
            .distinct()
        )

    return render(
        request,
        'student/student_search.html',
        {'students': students, 'query': query}
    )
