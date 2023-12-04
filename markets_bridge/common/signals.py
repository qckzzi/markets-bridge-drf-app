from django.db.models.signals import (
    post_save,
    pre_save,
)
from django.dispatch import (
    receiver,
)

from common.models import (
    CategoryMatching,
    CharacteristicMatching,
    CharacteristicValueMatching,
)
from common.services import (
    get_recipient_category_id_by_category_mathing_id,
)
from recipient.models import (
    Characteristic,
    CharacteristicValue,
)
from recipient.utils import (
    update_recipient_attributes,
)


@receiver(pre_save, sender=CategoryMatching)
def category_matching_pre_saved(sender, instance, *args, **kwargs):
    """Кеширует оригинальную категорию получателя для дальнейшей проверки на ее изменение."""

    original_recipient_category_id = None

    if instance.id:
        original_recipient_category_id = get_recipient_category_id_by_category_mathing_id(instance.id)

    instance.__original_recipient_category_id = original_recipient_category_id


@receiver(post_save, sender=CategoryMatching)
def category_matching_saved(sender, instance, created, **kwargs):
    """Проверяет, изменили ли категорию получателя.
    Если да, тогда актуализирует сопоставления характеристик и значений."""

    if instance.__original_recipient_category_id != instance.recipient_category_id:
        CharacteristicMatching.objects.filter(
            category_matching_id=instance.id,
        ).delete()

        if instance.recipient_category:
            update_recipient_attributes(instance.recipient_category.external_id, instance.id)
