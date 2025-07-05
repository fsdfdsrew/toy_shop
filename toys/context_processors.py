from django.utils import translation

def current_language(request):
    """Добавляет текущий язык в контекст шаблона"""
    return {
        'CURRENT_LANGUAGE': translation.get_language(),
    } 