from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.db import IntegrityError
from django.core.paginator import Paginator
from users.models import User
from .models import TutorProfile,Subject
from .forms import TutorProfileForm
from student.models import Student

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Prefetch

@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class TutorView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'tutor/tutor_dashboard.html'

    def get_template_names(self):
        # Switch template based on query param
        if self.request.GET.get('view') == 'enrolled_students':
            return ['tutor/enrolled_students.html']
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  

        # -----------------------------
        # Tutor Profile (Admin or Tutor)
        # -----------------------------
        tutor_profile = None
        if self.request.user.is_superuser:
            tutor_profile = TutorProfile.objects \
                .prefetch_related("subjects", "courses") \
                .first()
        else:
            tutor_profile = getattr(self.request.user, 'tutorprofile', None)

        # -----------------------------
        # If tutor profile exists
        # -----------------------------
        if tutor_profile:
            # Reuse querysets instead of calling .all()/.count() separately
            tutor_subjects_qs = tutor_profile.subjects.all()
            tutor_courses_qs = tutor_profile.courses.all()

            # Prefetch enrolled_courses + user to avoid N+1 in template
            enrolled_students_qs = Student.objects.filter(
                enrolled_courses__in=tutor_courses_qs
            ).select_related("user").prefetch_related("enrolled_courses").distinct()

            context.update({
                "tutor_subjects": tutor_subjects_qs,
                "subjects_count": tutor_subjects_qs.count(),
                "tutor_courses": tutor_courses_qs,
                "courses_count": tutor_courses_qs.count(),
                "enrolled_students": enrolled_students_qs,
                "students_count": enrolled_students_qs.count(),
            })
        else:
            context.update({
                "tutor_subjects": [],
                "subjects_count": 0,
                "tutor_courses": [],
                "courses_count": 0,
                "enrolled_students": [],
                "students_count": 0,
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

    # ✅ Agar tutor ka profile already exist karta hai
    def dispatch(self, request, *args, **kwargs):
        if TutorProfile.objects.filter(user=request.user).exists():
            messages.warning(request, "You already have a profile. You can update it instead.")
            return redirect('home_page')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user  # profile ko user ke saath link karo

        try:
            response = super().form_valid(form)

            # ✅ Subjects hidden inputs se lo
            new_subjects = self.request.POST.getlist("new_subjects")
            if new_subjects:
                for name in new_subjects:
                    name = name.strip().capitalize()
                    if name:
                        subject, created = Subject.objects.get_or_create(name=name)
                        form.instance.subjects.add(subject)

            messages.success(self.request, "Tutor profile created successfully!")
            return response

        except IntegrityError as e:
            if 'phone_number' in str(e):
                form.add_error('phone_number', "This phone number is already in use. Please use a different number.")
            else:
                messages.error(self.request, "An error occurred while saving the profile.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors and try again.")
        # Debugging ke liye console me errors print kar do
        for field, errors in form.errors.items():
            print(f"Field: {field}, Errors: {errors}")
        return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        return self.request.user.role == User.TUTOR

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('users:login' if not self.request.user.is_authenticated else 'home_page')

    def get_success_url(self):
        return reverse_lazy('home_page')

@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class TutorProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TutorProfile
    form_class = TutorProfileForm
    template_name = 'tutor/tutor_profile_create.html'
    success_url = reverse_lazy('home_page')
    
    def form_valid(self, form):
        form.instance.user = self.request.user

        response = super().form_valid(form)

        # ✅ Purane subjects clear kar ke naye set karo
        # form.instance.subjects.clear()

        # ✅ Subjects hidden inputs se lo
        new_subjects = self.request.POST.getlist("new_subjects")
        if new_subjects:
            for name in new_subjects:
                name = name.strip().capitalize()
                if name:
                    subject, created = Subject.objects.get_or_create(name=name)
                    form.instance.subjects.add(subject)

        messages.success(self.request, "Tutor profile updated successfully!")
        return response

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
    paginate_by=2
    def get_queryset(self):
        tutors = cache.get("all_tutors")
        if not tutors:
           print("🔥 DB se tutors fetch ho rahe hain (cache MISS)")
           tutors = list(
              TutorProfile.objects
              .select_related("user")   # OneToOne / ForeignKey relations
              .prefetch_related("subjects", "courses")  # ManyToMany relations
            )
           cache.set("all_tutors", tutors, 60)
        else:
           print("✅ Cache HIT (DB skip)")

        return tutors

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



def search_tutors(request):
    query = request.GET.get('query', '').strip()

    tutors = TutorProfile.objects.none()
    if query and len(query) >= 3:
        tutors = TutorProfile.objects.filter(
            Q(user__first_name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(subjects__name__icontains=query) |
            Q(courses__title__icontains=query)
        ).distinct()

    # ✅ pagination
    paginator = Paginator(tutors, 5)  # 5 tutors per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "tutor/tutor_search_results.html",
        {
            "tutors": page_obj,  # loop ke liye
            "page_obj": page_obj,  # pagination ke liye
            "query": query,
        }
    )
