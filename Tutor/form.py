from django import forms
from .models import TutorProfile

class TutorProfileForm(forms.ModelForm):
    class Meta:
        model = TutorProfile
        fields = ['bio', 'education', 'certifications', 'subjects', 'experience_years', 'hourly_rate', 'languages_spoken', 'profile_picture', 'available_from', 'available_until']
