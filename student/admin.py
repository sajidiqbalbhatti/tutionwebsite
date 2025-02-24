from django.contrib import admin
from .models import Student


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'date_of_birth', 'parent_name', 'created_at','display_enrolled_courses')
    def display_enrolled_courses(self, obj):
        """Display enrolled courses as a comma-separated list."""
        return ", ".join([course.title for course in obj.enrolled_courses.all()])  # Change `title` to the actual course field name in Course model

    display_enrolled_courses.short_description = "Enrolled Courses"
    list_filter = ('name','created_at')  # Filters in the admin sidebar
    search_fields = ('name', 'phone', 'parent_name')  # Search box for specific fields
    readonly_fields = ('created_at', 'updated_at')  # Mark fields as read-only
    fieldsets = (
        ("Student Information", {
            'fields': ('user', 'name',  'date_of_birth', 'phone', 'address')
        }),
        ("Parent Information", {
            'fields': ('parent_name', 'parent_contact')
        }),
        ("Additional Details", {
            'fields': ('profile_picture', 'enrolled_courses')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at')
        }),
    )


# Register the model and custom admin
admin.site.register(Student, StudentAdmin)
