from django.apps import AppConfig

class TutorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Tutor'  # ✅ Use lowercase app name (matches your folder name)

    def ready(self):
        import Tutor.signals  # 👈 Import your signals here
