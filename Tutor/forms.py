from django import forms
from .models import TutorProfile, Subject

class TutorProfileForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = TutorProfile
        fields = ['name', 'bio', 'education','subjects','certifications','phone_number','profile_picture','id_card_number','id_card_picture','city','experience_years', 'hourly_rate', 
                  'languages_spoken','available_from', 'available_until','is_featured']
