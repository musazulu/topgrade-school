import os
import sys

if __name__ == '__main__':
    # Determine environment (default to 'development')
    ENV = os.environ.get('DJANGO_ENV', 'development')

    if ENV == 'production':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'topgrade_school.settings_production')
    else:
        # Use the standard settings.py for development
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'topgrade_school.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)