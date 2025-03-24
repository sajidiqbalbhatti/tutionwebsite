from django import forms
from .models import Assignment, AssignmentSubmission

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'course', 'due_date', 'max_marks', 'file']
    
    # Custom validation for the file field to ensure the user uploads a file
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file:
            raise forms.ValidationError('Please upload a file.')
        # You can also add additional validation like file size or type if necessary
        if file.size > 5 * 1024 * 1024:  # 5 MB file size limit
            raise forms.ValidationError('File size exceeds the 5MB limit.')
        return file


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['submitted_file', 'submitted_text']
    
    # Custom validation for the submitted file to ensure it's uploaded
    def clean_submitted_file(self):
        file = self.cleaned_data.get('submitted_file')
        if not file:
            raise forms.ValidationError('Please upload your assignment submission.')
        # You can also add additional validation for file size or type
        if file.size > 5 * 1024 * 1024:  # 5 MB file size limit
            raise forms.ValidationError('File size exceeds the 5MB limit.')
        return file

class GradeAssignmentForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['marks_obtained', 'feedback']