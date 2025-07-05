from django.apps import AppConfig


class ToysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'toys'
    verbose_name = 'Игрушки'

    def ready(self):
        import toys.translation  # Импортируем переводы
