import sys
import os

# Replace this with the path to your project folder on PythonAnywhere
path = '/home/sajidiqbal/tuition_project'
if path not in sys.path:
    sys.path.append(path)

# Replace this with your actual Django settings module (folder.settings)
os.environ['DJANGO_SETTINGS_MODULE'] = 'tuition_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
