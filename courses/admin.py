from django.contrib import admin  
from .models import Category, Level, Subject, Course,LearningModeOption

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'level', 'created_at', 'updated_at')
    search_fields = ('subject_name',)
    list_filter = ('level',)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title','created_at', 'updated_at')  # Removed 'price'
    search_fields = ('title', 'tutor__username', 'category__name', 'level__choice', 'subject__subject_name')
    list_filter = ('created_at', 'course_level')


# Register models with their respective admin classes
admin.site.register(Category, CategoryAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(LearningModeOption)
