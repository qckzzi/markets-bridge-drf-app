from django.apps import (
    AppConfig,
)


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'
    verbose_name = 'Общее'

    def ready(self):
        from common.signals import (
            cache_original_recipient_category,
            validate_category_matching,
        )
