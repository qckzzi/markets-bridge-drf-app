from django.apps import (
    AppConfig,
)


class ProviderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'provider'
    verbose_name = 'Поставщик'

    def ready(self):
        from provider.signals import (
            validate_category,
        )
