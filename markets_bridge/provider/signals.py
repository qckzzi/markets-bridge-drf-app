from django.db.models.signals import (
    post_save,
)
from django.dispatch import (
    receiver,
)

from provider.models import (
    Category,
)
from provider.services import (
    create_category_mathing,
)


@receiver(post_save, sender=Category)
def validate_category(sender, instance, created, **kwargs):
    """При создании категории создает запись сопоставления."""

    if created:
        create_category_mathing(category_id=instance.pk)
