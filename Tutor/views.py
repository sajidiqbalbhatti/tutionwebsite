from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control

from users.models import User
from .models import TutorProfile
from .forms import TutorProfileForm
from student.models import Student

@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class TutorView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'tutor/tutor_dashboard.html'

    def get_template_names(self):
        return ['tutor/enrolled_students.html'] if self.request.GET.get('view') == 'enrolled_students' else [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  
        tutor_profile = getattr(self.request.user, 'tutorprofile', None)

        if tutor_profile:
            tutor_courses = tutor_profile.courses.all()
            enrolled_students = Student.objects.filter(enrolled_courses__in=tutor_courses).distinct()
            context.update({
                'tutor_subjects': tutor_profile.subjects.all(),
                'subjects_count': tutor_profile.subjects.count(),
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
        return self.request.user.role == User.TUTOR

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('users:login' if not self.request.user.is_authenticated else 'home_page')

@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class TutorProfileCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = TutorProfile
    form_class = TutorProfileForm
    template_name = 'tutor/tutor_profile_create.html'
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors and try again.")
        return self.render_to_response(self.get_context_data(form=form))
    
    def test_func(self):
        return self.request.user.role == User.TUTOR

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('users:login' if not self.request.user.is_authenticated else 'home_page')

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
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('users:login' if not self.request.user.is_authenticated else 'home_page')

class TutorProfileDetailView(DetailView):
    model = TutorProfile
    template_name = 'tutor/tutor_profile_detail.html'
    context_object_name = 'tutor'

class TutorProfileListView(ListView):
    model = TutorProfile
    template_name = 'tutor/tutor_profile_list.html'
    context_object_name = 'tutors'

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
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('users:login' if not self.request.user.is_authenticated else 'home_page')

# Tutor Search View
def search_tutors(request):
    query = request.GET.get('query', '').strip()
    tutors = TutorProfile.objects.filter(
        Q(user__first_name__icontains=query) | Q(subjects__name__icontains=query)
    ).distinct() if query and len(query) >= 3 else TutorProfile.objects.none()
    
    return render(request, 'tutor/tutor_search_results.html', {'tutors': tutors, 'query': query})
