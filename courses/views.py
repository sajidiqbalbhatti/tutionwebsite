from email.charset import QP
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.shortcuts import render, redirect

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
        # Automatically assign the logged-in user as the course creator
        form.instance.tutor = self.request.user  # Adjust if assigning to students
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
class CourseDetailView( DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"


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