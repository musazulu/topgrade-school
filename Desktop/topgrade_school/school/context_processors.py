from .models import SchoolInfo


def school_info(request):
    """Add school info to all templates"""
    info = SchoolInfo.objects.first()
    return {
        'school_info': info,
        'school_name': info.name if info else 'Top Grade Education Centre',
        'school_phone': info.phone if info else '',
        'school_email': info.email if info else '',
    }