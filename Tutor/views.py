from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.db import IntegrityError

from users.models import User
from .models import TutorProfile
from .forms import TutorProfileForm
from student.models import Student

@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class TutorView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'tutor/tutor_dashboard.html'

    def get_template_names(self):
        # Check if we should display the enrolled students view
        return ['tutor/enrolled_students.html'] if self.request.GET.get('view') == 'enrolled_students' else [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  

        # Get the tutor profile for the logged-in user
        tutor_profile = None
        if self.request.user.is_superuser:
            # If admin is accessing, you can pick any tutor profile (or skip this logic)
           tutor_profile = TutorProfile.objects.first()  # or customize this logic
        else:
           tutor_profile = getattr(self.request.user, 'tutorprofile', None)

           # Use tutor_profile safely now

    

        if tutor_profile:
            # Get all courses associated with the tutor
            tutor_courses = tutor_profile.courses.all()
            

            # Get students enrolled in these courses
            enrolled_students = Student.objects.filter(enrolled_courses__in=tutor_courses).distinct()

            context.update({
                'tutor_subjects': tutor_profile.subjects.all(),
                'subjects_count': tutor_profile.subjects.count(),
                'tutor_courses': tutor_courses.count(),
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
        # Ensure that the logged-in user has a role of 'TUTOR'
         return self.request.user.role == User.TUTOR or self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('users:login')
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('users:login')
@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class TutorProfileCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = TutorProfile
    form_class = TutorProfileForm
    template_name = 'tutor/tutor_profile_create.html'
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            response = super().form_valid(form)
            messages.success(self.request, "Tutor profile created successfully!")
            return response
        except IntegrityError as e:
            if 'Tutor_tutorprofile.phone_number' in str(e):
                form.add_error('phone_number', "This phone number is already in use. Please use a different number.")
            else:
                messages.error(self.request, "An error occurred while saving the profile.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors and try again.")
            # Optionally, log form errors for debugging
        for field, errors in form.errors.items():
            print(f"Field: {field}, Errors: {errors}")
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
    success_url = reverse_lazy('home_page')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "successfully update ")

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors and try again.")
        return self.render_to_response(self.get_context_data(form=form))

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
        Q(user__first_name__icontains=query) | Q(subjects__name__icontains=query)|
        Q(courses__title__icontains=query)
    ).distinct() if query and len(query) >= 3 else TutorProfile.objects.none()
    
    return render(request, 'tutor/tutor_search_results.html', {'tutors': tutors, 'query': query})
