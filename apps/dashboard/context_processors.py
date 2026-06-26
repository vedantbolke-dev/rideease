from apps.bikes.models import ContactMessage


def unread_messages(request):
    """Injects unread contact message count for admin navbar badge."""
    if request.user.is_authenticated and request.user.is_staff:
        count = ContactMessage.objects.filter(is_read=False).count()
        return {'unread_messages_count': count}
    return {'unread_messages_count': 0}


def developer_info(request):
    """Injects student/developer metadata globally into all templates."""
    from django.conf import settings
    return {
        'DEVELOPER_NAME': getattr(settings, 'DEVELOPER_NAME', 'Lead Developer'),
        'PARTNER_NAME': getattr(settings, 'PARTNER_NAME', 'Associate Developer'),
        'COLLEGE_NAME': getattr(settings, 'COLLEGE_NAME', 'Academy of Computer Science'),
        'ACADEMIC_YEAR': getattr(settings, 'ACADEMIC_YEAR', '2025-2026'),
    }

