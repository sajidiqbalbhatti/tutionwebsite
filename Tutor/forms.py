from django import forms
from .models import TutorProfile, Subject

class TutorProfileForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = TutorProfile
        fields = ['name', 'bio', 'education','subjects', 'certifications', 'experience_years', 'hourly_rate', 
                  'languages_spoken', 'profile_picture', 'available_from', 'available_until']
