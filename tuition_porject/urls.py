from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notifications/', include('Notification.urls')),
    path('users/', include('users.urls')),
    path('', include('Home.urls')),
    path('courses/', include('courses.urls')),
    path('student/', include('student.urls')),
    path('tutor/', include('Tutor.urls', namespace='tutor')),
    path('contact/', include('contact.urls')),
    path('assessments/', include('assignments.urls')),
]

# Always serve static files (Django development or via WhiteNoise in production)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
