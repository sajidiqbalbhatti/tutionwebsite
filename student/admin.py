from django.contrib import admin
from .models import Student, Course

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'enrolled_courses_display')  # Show enrolled courses in admin

    def enrolled_courses_display(self, obj):
        if obj.enrolled_courses.exists():
            return ", ".join([course.title for course in obj.enrolled_courses.all()])
        return "-"

    enrolled_courses_display.short_description = "Enrolled Courses"


