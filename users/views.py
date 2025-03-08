from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
import json

from .forms import UserSignupForm
from .models import User
from courses.models import Course

# Admin Dashboard View
class AdminView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'users/admin_dashboard.html'

    def test_func(self):
        return self.request.user.role == User.ADMIN

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('users:login')
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Generate last 6 months dynamically
        months = [(now() - relativedelta(months=i)).strftime('%b %Y') for i in reversed(range(6))]
        month_year_pairs = [(now() - relativedelta(months=i)) for i in reversed(range(6))]

        tutor_signups = [
            User.objects.filter(role=User.TUTOR, date_joined__year=dt.year, date_joined__month=dt.month).count()
            for dt in month_year_pairs
        ]
        student_signups = [
            User.objects.filter(role=User.STUDENT, date_joined__year=dt.year, date_joined__month=dt.month).count()
            for dt in month_year_pairs
        ]

        context.update({
            'total_users': User.objects.count(),
            'new_signups': User.objects.filter(date_joined__gte=now() - relativedelta(months=1)).count(),
            'total_courses': Course.objects.count(),
            'months': json.dumps(months),
            'tutor_signups': json.dumps(tutor_signups),
            'student_signups': json.dumps(student_signups),
        })
        
        return context

# Parent Dashboard View
class ParentView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'users/parent_dashboard.html'

    def test_func(self):
        return self.request.user.role == User.PARENT

# User Signup View
class UserSignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        return redirect(self.success_url)

# Role-Based Login View
class RoleBasedLoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, "Login successful!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)

    def get_success_url(self):
        role_redirects = {
            User.ADMIN: 'home_page',
            User.TUTOR: 'home_page',
            User.STUDENT: 'home_page',
            User.PARENT: 'users:parent_dashboard',
        }
        return reverse(role_redirects.get(self.request.user.role, 'home_page'))
