from django.apps import AppConfig


class ShiprocketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.shiprocket'

    # def ready(self):
    #     from . import scheduler
    #     scheduler.start()
