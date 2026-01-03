import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'topgrade_school.settings')  # ← CHANGE THIS

application = get_wsgi_application()