
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include


urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('notifications/', include('Notification.urls')),
    path('users/',include('users.urls')),
    path('',include('Home.urls')),
    path('courses/',include('courses.urls')),
    path('student/',include('student.urls')),
    path('tutor/',include('Tutor.urls',namespace='tutor')),
    path('contact/',include('contact.urls')),
  
    # path('live_classes/',include('live_classes.urls')),
    path('assessments/',include('assignments.urls')),

         
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # 👇 Manually serve media in production-like local testing (Render will need proper setup too)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)