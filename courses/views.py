from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Course
from courses.forms import CourseForm
from student.models import Student
from django.contrib.auth import get_user_model

User = get_user_model()

# ============================
# Course Creation View
# ============================
@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name="dispatch")
class CourseCreateView(LoginRequiredMixin, CreateView):
    """Allows tutors to create a new course."""
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_url = reverse_lazy("courses:course_list")

    def form_valid(self, form):
        """Assigns the tutor profile to the course upon creation."""
        tutor_profile = self.request.user.tutorprofile  
        form.instance.save()  
        form.instance.tutors.add(tutor_profile)  
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There were errors in your form. Please correct them and try again.")
        return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        return self.request.user.role == User.TUTOR

    def get_form(self, **kwargs):
        """Restricts course creation to authorized users only."""
        if self.request.user.role not in User.TUTOR:
            raise PermissionDenied("Only authorized users can create courses.")
        return super().get_form(**kwargs)

# ============================
# Course List View
# ============================
class CourseListView(ListView):
    """Displays a list of all courses."""
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"

# ============================
# Course Detail View
# ============================
@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name="dispatch")
class CourseDetailView(LoginRequiredMixin, DetailView):
    """Displays detailed information about a course."""
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        """Adds enrollment status to context data."""
        context = super().get_context_data(**kwargs)
        context["is_enrolled"] = self.request.user in self.object.students.all()
        return context

# ============================
# Course Update View
# ============================
@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name="dispatch")
class CourseUpdateView(LoginRequiredMixin, UpdateView):
    """Allows tutors to update their courses."""
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_url = reverse_lazy("courses:course_list")

    def get_object(self, queryset=None):
        """Ensures tutors can only update their own courses."""
        return get_object_or_404(Course, pk=self.kwargs["pk"], created_by=self.request.user)

# ============================
# Course Delete View
# ============================
@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name="dispatch")
class CourseDeleteView(LoginRequiredMixin, DeleteView):
    """Allows tutors to delete their courses."""
    model = Course
    template_name = "courses/course_delete.html"
    success_url = reverse_lazy("courses:course_list")

    def get_queryset(self):
        """Restricts deletion to tutors or enrolled students."""
        return Course.objects.filter(tutor=self.request.user) | Course.objects.filter(students=self.request.user)

    def get_object(self, queryset=None):
        """Ensures the object exists and handles non-existent cases."""
        return get_object_or_404(Course, pk=self.kwargs["pk"])

# ============================
# Search Functionality
# ============================
def SearchResultsView(request):
    """Handles course search functionality."""
    query = request.GET.get('q', '').strip()  # Get the search query, remove extra spaces
    courses = Course.objects.none()  # Default to an empty queryset

    if query and len(query) >= 3:
        courses = Course.objects.filter(
            Q(title__icontains=query) |       # Search by course title
            Q(teacher__name__icontains=query) |  # Search by teacher name
            Q(mode__mode__icontains=query)   # Search by mode (ManyToManyField)
        ).distinct()

    return render(request, 'courses/course_search.html', {'courses': courses, 'query': query})

# ============================
# Course Enrollment View
# ============================
class EnrollInCourseView(LoginRequiredMixin, View):
    """Handles student enrollment in courses."""
    
    def post(self, request, course_id, *args, **kwargs):
        print("Extracted Course ID from URL:", course_id)

        if not course_id:
            messages.error(request, "Invalid course selection.")
            return redirect("courses:course_list")

        course = get_object_or_404(Course, id=course_id, is_active=True)

        if request.user.role.lower() == "student":
            try:
                student = Student.objects.get(user=request.user)
                
                if student.enrolled_courses.filter(id=course.id).exists():
                    messages.warning(request, f"You are already enrolled in {course.title}.")
                else:
                    student.enrolled_courses.add(course)
                    messages.success(request, f"You have successfully enrolled in {course.title}.")
                    
            except Student.DoesNotExist:
                messages.error(request, "Student profile not found. Please complete your profile.")
        else:
            messages.error(request, "Only students can enroll in courses.")

        return redirect("courses:course_detail", course.id)
