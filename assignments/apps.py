from django.apps import AppConfig


class AssignmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assignments'
    
    # students/apps.py
    def ready(self):
        import assignments.signals

