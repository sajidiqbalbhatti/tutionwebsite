from django.contrib import admin
from .models import Assignment, AssignmentSubmission


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'tutor', 'due_date', 'max_marks', 'created_at')
    search_fields = ('title', 'course__name', 'tutor__user__username')
    list_filter = ('course', 'due_date')
    ordering = ('-created_at',)


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'is_late', 'graded', 'marks_obtained')
    search_fields = ('assignment__title', 'student__user__username')
    list_filter = ('is_late', 'graded')
    ordering = ('-submitted_at',)
    readonly_fields = ('submitted_at', 'is_late')  # Prevents editing these fields manually in admin


# Alternative way (if not using decorators)
# admin.site.register(Assignment, AssignmentAdmin)
# admin.site.register(AssignmentSubmission, AssignmentSubmissionAdmin)
