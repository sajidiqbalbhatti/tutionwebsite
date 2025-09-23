from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from .models import Course
from courses.forms import CourseForm
from student.models import Student

User = get_user_model()

# ============================
# Course Creation View
# ============================
# @method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name="dispatch")
class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_url = reverse_lazy("courses:course_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  
        return kwargs

    def form_valid(self, form):
        if not hasattr(self.request.user, 'tutorprofile'):
            messages.error(self.request, "You don't have a tutor profile.")
            return self.form_invalid(form)

        tutor_profile = self.request.user.tutorprofile
        form.instance.created_by = self.request.user  

        response = super().form_valid(form)  
        tutor_profile.courses.add(self.object)  # link tutor with course

        return response

    def test_func(self):
        return hasattr(self.request.user, 'tutorprofile')


# ============================
# Course List View
# ============================



# @method_decorator(cache_page(60 * 1), name='dispatch')  # 1 min ke liye cache
class CourseListView(ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"
    
    
    def get_queryset(self):
        courses = cache.get("all_courses")

        if not courses:
            print("🔥 DB se query chal rahi hai (cache MISS)")
            # Evaluate queryset into a list (so actual objects cache ho jayein)
            courses = list(Course.objects.select_related("created_by"))
            cache.set("all_courses", courses, 60)  # 60 sec ke liye cache
        else:
            print("✅ Cache HIT (DB skip)")

        return courses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for course in context['courses']:
            course.teacher_name = course.created_by.username
        return context



# ============================
# Course Detail View
# ============================
# @method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name="dispatch")
# @method_decorator(cache_page(60 * 1), name='dispatch')
class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"

    def get_queryset(self):
        # ✅ Fix N+1: prefetch tutors & students
        return Course.objects.prefetch_related("tutors", "students")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tutors'] = self.object.tutors.all()
        context["is_enrolled"] = self.request.user in self.object.students.all()
        return context


# ============================
# Course Update View
# ============================
# @method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name="dispatch")
class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_url = reverse_lazy("courses:course_list")
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if not hasattr(self.request.user, 'tutorprofile'):
            messages.error(self.request, "You don't have a tutor profile.")
            return self.form_invalid(form)
           
        tutor_profile = self.request.user.tutorprofile
        form.instance.teacher = tutor_profile
        form.instance.created_by = self.request.user
        response = super().form_valid(form)

        # ✅ Cache clear kar do taake fresh data load ho next time
        cache.delete("all_courses")
        print("🗑️ Cache cleared after course update")

        return response
        

    def get_object(self, queryset=None):
        return get_object_or_404(Course, pk=self.kwargs["pk"], created_by=self.request.user)


# ============================
# Course Delete View
# ============================
# @method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name="dispatch")
class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = "courses/course_delete.html"
    success_url = reverse_lazy("courses:course_list")

    def get_queryset(self):
        return Course.objects.filter(tutor=self.request.user) | Course.objects.filter(students=self.request.user)

    def get_object(self, queryset=None):
        return get_object_or_404(Course, pk=self.kwargs["pk"])
    
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)

        # ✅ yaha cache clear karo
        cache.delete("all_courses")
        print("🗑️ Cache cleared after course delete")

        return response


# ============================
# Search Functionality
# ============================
def SearchResultsView(request):
    query = request.GET.get('q', '').strip()
    courses = Course.objects.none()

    if query and len(query) >= 3:
        courses = (
            Course.objects.prefetch_related("tutors", "mode")  # ✅ Fix N+1
            .filter(
                Q(title__icontains=query) |
                Q(tutors__name__icontains=query) |
                Q(mode__mode__icontains=query)
            )
            .distinct()
        )

    return render(request, 'courses/course_search.html', {'courses': courses, 'query': query})


# ============================
# Course Enrollment View
# ============================
class EnrollInCourseView(LoginRequiredMixin, View):
    def post(self, request, course_id, *args, **kwargs):
        if not course_id:
            messages.error(request, "Invalid course selection.")
            return redirect("courses:course_list")

        course = get_object_or_404(Course, id=course_id, is_active=True)

        if request.user.role.lower() == "student":
            try:
                student = Student.objects.prefetch_related("enrolled_courses").get(user=request.user)  # ✅ Fix N+1
                
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
