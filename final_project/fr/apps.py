from django.apps import AppConfig


class FrConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fr'

    def ready(self):
        import fr.signals
