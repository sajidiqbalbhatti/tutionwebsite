from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'phone', 'address','date_of_birth','parent_name','parent_contact','category', 'level', 'profile_picture']

    
    
