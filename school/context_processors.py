from .models import SchoolInfo


def school_info(request):
    """
    Add school info to all templates.
    Safe fallback if no SchoolInfo record exists.
    """
    try:
        info = SchoolInfo.objects.first()
        if info:
            return {
                'school_info': info,
                'school_name': info.name,
                'school_phone': info.phone,
                'school_email': info.email,
            }
        else:
            # No record in database — return defaults
            return {
                'school_info': None,
                'school_name': 'Top Grade Education Centre',
                'school_phone': '',
                'school_email': '',
            }
    except Exception:
        # In case of any error (e.g. DB not ready), return safe defaults
        return {
            'school_info': None,
            'school_name': 'Top Grade Education Centre',
            'school_phone': '',
            'school_email': '',
        }