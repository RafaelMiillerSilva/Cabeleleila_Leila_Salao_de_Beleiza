import os
from django.core.wsgi import get_wsgi_application
from django.contrib.auth import get_user_model

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'CabeleleilaLeila.settings')

User = get_user_model()
if not User.objects.filter(username='leila').exists():
    User.objects.create_superuser('leila', 'leila@email.com', 'leila123')

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_wsgi_application()




# ---------------------------------------------