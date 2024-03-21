from django.apps import AppConfig

class ScreeningroomsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'screeningrooms'

    def ready(self):
        # Import signals to ensure they are recognized and connected by Django at startup
        import screeningrooms.signals
