from django.apps import (
    AppConfig,
)


class RecipientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipient'
    verbose_name = 'Получатель'
