
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include

from .views import EducationHomepage


urlpatterns = [
    path('', EducationHomepage.as_view(),name='home_page'),
    path('admin/', admin.site.urls),
    path('users/',include('users.urls')),
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