from django.apps import (
    AppConfig,
)


class ProviderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'provider'
    verbose_name = 'Поставщик'

    def ready(self):
        from provider.signals import (
            category_saved,
            characteristic_saved,
            characteristic_value_saved,
            product_saved,
        )
