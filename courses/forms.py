from django import forms
from .models import Course, LearningModeOption

class CourseForm(forms.ModelForm):
    mode = forms.ModelMultipleChoiceField(
        queryset=LearningModeOption.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Course
        fields = ('teacher','title', 'description', 'course_level','thumbnail','mode', 'duration', 'fee', 'start_date', 'end_date', 'is_active','created_by',)

    def save(self, commit=True):
        course = super().save(commit=False)  # Save course instance without committing to DB
        if commit:
            course.save()  # Save course instance
            self.save_m2m()  # Save many-to-many relationships
        return course
