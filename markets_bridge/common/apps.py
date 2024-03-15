from django.apps import (
    AppConfig,
)


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'
    verbose_name = 'Система'

    def ready(self):
        from common.signals import (
            category_matching_pre_saved,
            category_matching_saved,
            characteristic_matching_pre_saved,
            characteristic_matching_saved,
        )
