from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone', 'category', 'level', 'created_at')
    list_filter = ('category', 'level', 'created_at')
    search_fields = ('user__username', 'name', 'phone', 'parent_name')
    ordering = ('-created_at',)
    filter_horizontal = ('enrolled_courses', 'enrolled_tutors')

admin.site.register(Student, StudentAdmin)
