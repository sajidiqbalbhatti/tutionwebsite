from django.contrib import admin
from .models import TutorProfile, Subject,Enrollment

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']

class TutorProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'name',
        'education',
        'get_subjects',  # Custom method for subjects
        'hourly_rate',
        'rating',
        'available_from',
        'available_until',
    )
    search_fields = ('user__username', 'name', 'education', 'subjects__name')  # Use subjects__name for searching related field
    list_filter = ('rating', 'education')
    ordering = ('user',)

    def get_subjects(self, obj):
        """Display subjects as a comma-separated string."""
        return ", ".join([subject.name for subject in obj.subjects.all()])
    
    get_subjects.short_description = 'Subjects'  # Column header in admin list view

admin.site.register(TutorProfile, TutorProfileAdmin)
admin.site.register(Enrollment)
