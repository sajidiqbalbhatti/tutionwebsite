# tutor/forms.py
from django import forms
from .models import TutorProfile

class TutorProfileForm(forms.ModelForm):
    new_subjects = forms.CharField(
        required=True,   # ab required kar diya
        help_text="Enter subjects separated by commas (e.g. Math, Physics, English)"
    )

    class Meta:
        model = TutorProfile
        exclude = ['user', 'subjects','courses']   # 👈 subjects field ko hata diya
