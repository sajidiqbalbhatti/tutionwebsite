from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView, CreateView, UpdateView, DetailView, ListView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control

from users.models import User
from .models import TutorProfile, Subject
from .forms import TutorProfileForm
from student.models import Student
from courses.models import Course

# Tutor Dashboard View
@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class TutorView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'tutor/tutor_dashboard.html'

    def get_template_names(self):
        """Chooses the template based on the 'view' query parameter."""
        view_type = self.request.GET.get('view')
        return ['tutor/enrolled_students.html'] if view_type == 'enrolled_students' else ['tutor/tutor_dashboard.html']

    def get_context_data(self, **kwargs):
        """Fetches tutor-related data for the dashboard."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  
        tutor_profile = getattr(self.request.user, 'tutorprofile', None)

        if tutor_profile:
            tutor_subjects = tutor_profile.subjects.all()
            tutor_courses = Course.objects.filter(subject__id__in=tutor_subjects.values_list('id', flat=True))
            enrolled_students = Student.objects.filter(enrolled_courses__in=tutor_courses).distinct()
            
            context.update({
                'tutor_subjects': tutor_subjects,
                'subjects_count': tutor_subjects.count(),
                'tutor_courses': tutor_courses,
                'enrolled_students': enrolled_students,
                'students_count': enrolled_students.count(),
            })
        else:
            context.update({
                'tutor_subjects': [],
                'subjects_count': 0,
                'tutor_courses': [],
                'enrolled_students': [],
                'students_count': 0,
            })

        return context

    def test_func(self):
        """Restricts access to users with the 'TUTOR' role."""
        return self.request.user.role == User.TUTOR

    def handle_no_permission(self):
        """Handles unauthorized access attempts."""
        if not self.request.user.is_authenticated:
            return redirect('users:login')
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('home_page')

# Tutor Profile Creation View
@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')

class TutorProfileCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = TutorProfile
    form_class = TutorProfileForm
    template_name = 'tutor/tutor_profile_create.html'
    success_url = reverse_lazy('home_page')
    
    

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
        return self.request.user.role == User.TUTOR

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('users:login')
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('home_page')

# Tutor Profile Update View
@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class TutorProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TutorProfile
    form_class = TutorProfileForm
    template_name = 'tutor/tutor_profile_create.html'
    success_url = reverse_lazy('Tutor:tutor-profile-list')

    def get_object(self):
        return get_object_or_404(TutorProfile, user=self.request.user)

    def test_func(self):
        return self.request.user.role == User.TUTOR

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('users:login')
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('home_page')

# Tutor Profile Detail View
class TutorProfileDetailView(DetailView):
    model = TutorProfile
    template_name = 'tutor/tutor_profile_detail.html'
    context_object_name = 'tutor'

# Tutor Profile List View
class TutorProfileListView(ListView):
    model = TutorProfile
    template_name = 'tutor/tutor_profile_list.html'
    context_object_name = 'tutor'

    def get_queryset(self):
        return TutorProfile.objects.all()

# Tutor Profile Delete View
@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class TutorProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TutorProfile
    template_name = 'tutor/tutor_profile_confirm_delete.html'
    success_url = reverse_lazy('Tutor:tutor-profile-list')
    
    def get_object(self):
        return get_object_or_404(TutorProfile, user=self.request.user)
    
    def test_func(self):
        return self.request.user.role == User.TUTOR

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('users:login')
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('home_page')

# Tutor Search Function

def search_tutors(request):
    """Allows users to search for tutors by name or subject."""
    query = request.GET.get('query', '').strip()
    tutors = TutorProfile.objects.none()
    
    if query and len(query) >= 3:
        tutors = TutorProfile.objects.filter(
            Q(user__first_name__icontains=query) | Q(subjects__name__icontains=query)
        ).distinct()
    
    return render(request, 'tutor/tutor_search_results.html', {'tutors': tutors, 'query': query})
