from django.apps import AppConfig


class AutolotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'autolot'

    def ready(self):
        from . import signals
