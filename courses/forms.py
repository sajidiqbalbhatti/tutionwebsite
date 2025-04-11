from django import forms
from .models import Course, LearningModeOption

class CourseForm(forms.ModelForm):
    # Show Learning Modes as checkboxes
    mode = forms.ModelMultipleChoiceField(
        queryset=LearningModeOption.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Course
        fields = (
            'title', 'description', 
            'thumbnail', 'course_level', 'mode', 'duration', 'fee',
            'start_date', 'end_date', 'location', 'content',
            'is_featured', 'is_active', 'created_by'
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # User from view
        super().__init__(*args, **kwargs)

        if user:
            # Set 'created_by' to the logged-in user (you still want to do this)
            self.fields['created_by'].initial = user

        # Disable 'created_by' field from being edited manually
        self.fields['created_by'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        course = super().save(commit=False)

        if commit:
            course.save()
            self.save_m2m()  # Save ManyToMany fields (like 'mode')

        return course
