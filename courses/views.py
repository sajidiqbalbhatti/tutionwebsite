from email.charset import QP
from urllib import request
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView,View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.shortcuts import render, redirect
from student.models import Student

from django.db.models import Q


from courses.forms import CourseForm

from .models import Course

User = get_user_model()


@method_decorator(
    cache_control(no_cache=True, must_revalidate=True, no_store=True), name="dispatch"
)
class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_url = reverse_lazy("courses:course_list")
    
    

    def form_valid(self, form):
        tutor_profile = self.request.user.tutorprofile  # Get tutor profile
        form.instance.save()  # Save the course first
        form.instance.tutors.add(tutor_profile)  # Add tutor to ManyToManyField
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There were errors in your form. Please correct them and try again.")
        return self.render_to_response(self.get_context_data(form=form))
    
    def test_func(self):
        return self.request.user.role == User.TUTOR

    def get_form(self, **kwargs):
        # Allow only tutors or students to create courses
        if self.request.user.role not in User.TUTOR:
            raise PermissionDenied("Only authorized users can create courses.")
        return super().get_form(**kwargs)

class CourseListView( ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"
    
   
    # def get_queryset(self):
    #     """Filter courses by creator or category."""
    #     queryset = Course.objects.filter(created_by=self.request.user)
    #     category = self.request.GET.get("category")
    #     if category:
    #         queryset = queryset.filter(category__name=category)
    #     return queryset


@method_decorator(
    cache_control(no_cache=True, must_revalidate=True, no_store=True), name="dispatch"
)
class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_enrolled"] = self.request.user in self.object.students.all()
        # context["students_count"] = self.object.students.count() 
        return context

    


@method_decorator(
    cache_control(no_cache=True, must_revalidate=True, no_store=True), name="dispatch"
)
class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_url = reverse_lazy("courses:course_list")

    def get_object(self, queryset=None):
        # Ensure the user can only edit their own courses
        return get_object_or_404(
            Course, pk=self.kwargs["pk"], created_by=self.request.user
        )


@method_decorator(
    cache_control(no_cache=True, must_revalidate=True, no_store=True), name="dispatch"
)
class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = "courses/course_delete.html"
    success_url = reverse_lazy("courses:course_list")

    def get_queryset(self):
        # Allow only tutors or enrolled students to delete their own courses
        return Course.objects.filter(tutor=self.request.user) | Course.objects.filter(
            students=self.request.user
        )

    def get_object(self, queryset=None):
        # Ensure the object exists and handle the case if not
        return get_object_or_404(Course, pk=self.kwargs["pk"])


from django.shortcuts import render
from django.db.models import Q
from .models import Course

def SearchResultsView(request):
    query = request.GET.get('q', '').strip()  # Ensure correct key and remove spaces
    courses = Course.objects.none()  # Initialize empty queryset

    if query and len(query) >= 3:
        courses = Course.objects.filter(
            Q(title__icontains=query)|   # Search by course title
            Q(teacher__name__icontains=query)   # Search by course title
            # Q(subject__name__icontains=query)  # Search by subject name
        ).distinct()

    return render(request, 'courses/course_search.html', {'courses': courses, 'query': query})
class EnrollInCourseView(LoginRequiredMixin, View):
    def post(self, request, course_id, *args, **kwargs):
        print("Extracted Course ID from URL:", course_id)

        # Validate course_id
        if not course_id:
            messages.error(request, "Invalid course selection.")
            return redirect("courses:course_list")

        # Get course or return error message
        course = get_object_or_404(Course, id=course_id, is_active=True)

        # Check if the user is a student
        if request.user.role.lower() == "student":
            try:
                student = Student.objects.get(user=request.user)
                
                # Check if already enrolled
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
