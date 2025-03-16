from django.views.generic import TemplateView
from Tutor.models import TutorProfile
from courses.models import Course  # Import Course model

class EducationHomepage(TemplateView):
    template_name = "Education/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tutors"] = TutorProfile.objects.filter(is_featured=True)[:3]  # Fetch all tutors
        context["courses"] = Course.objects.filter(is_featured=True)[:3]
 # Fetch all courses
        return context
