from django.apps import AppConfig


class MemedbConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "memedb"

    def ready(self) -> None:
        import memedb.signals.handlers
