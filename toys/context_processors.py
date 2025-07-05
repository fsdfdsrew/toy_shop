from django.utils import translation
from django.conf import settings

def current_language(request):
    """Добавляет текущий язык в контекст шаблона"""
    return {
        'CURRENT_LANGUAGE': request.LANGUAGE_CODE
    }

def media_url(request):
    """
    Adds media-related context variables to the context.
    """
    return {
        'MEDIA_URL': '/static/media/' if not settings.DEBUG else settings.MEDIA_URL
    } 