import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'topgrade_school.settings')  # ← Should be topgrade_school

application = get_asgi_application()