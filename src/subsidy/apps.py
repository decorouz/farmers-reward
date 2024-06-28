from django.apps import AppConfig


class SubsidyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "subsidy"

    def ready(self) -> None:
        import subsidy.signals.handlers  # noqa: F401
