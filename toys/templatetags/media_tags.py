from django import template
from django.conf import settings

register = template.Library()

@register.filter
def media_url(value):
    """
    Converts media URL to static URL in production
    """
    if not value:
        return ''
    if not settings.DEBUG:
        return str(value).replace('/media/', '/static/media/')
    return value 