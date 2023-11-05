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
    update_recipient_attributes,
)
from recipient.models import (
    Characteristic,
    CharacteristicValue,
)


@receiver(pre_save, sender=CategoryMatching)
def cache_original_recipient_category(sender, instance, *args, **kwargs):
    """Кеширует оригинальную категорию получателя для дальнейшей проверки на ее изменение."""

    original_recipient_category_id = None

    if instance.id:
        original_recipient_category_id = get_recipient_category_id_by_category_mathing_id(instance.id)

    instance.__original_recipient_category_id = original_recipient_category_id


@receiver(post_save, sender=CategoryMatching)
def validate_category_matching(sender, instance, created, **kwargs):
    """Проверяет, изменили ли категорию получателя.
    Если да, тогда актуализирует сопоставления характеристик и значений."""

    if instance.__original_recipient_category_id != instance.recipient_category_id:
        CharacteristicMatching.objects.filter(
            category_matching_id=instance.id,
        ).delete()

        update_recipient_attributes(instance.recipient_category.external_id)

        recipient_characteristic_ids = Characteristic.objects.filter(
            categories=instance.recipient_category_id,
        ).values_list(
            'id',
            flat=True,
        )

        char_matching_list = [
            CharacteristicMatching(category_matching_id=instance.id, recipient_characteristic_id=char_id)
            for char_id in recipient_characteristic_ids
        ]

        created_char_mathing_list = CharacteristicMatching.objects.bulk_create(char_matching_list)

        for char_mathing in created_char_mathing_list:
            recipient_char_value_ids = CharacteristicValue.objects.filter(
                characteristic_id=char_mathing.recipient_characteristic_id,
            ).values_list(
                'id',
                flat=True,
            )

            char_value_mathing_list = [
                CharacteristicValueMatching(
                    characteristic_matching_id=char_mathing.id,
                    recipient_characteristic_value_id=value_id,
                )
                for value_id in recipient_char_value_ids
            ]

            CharacteristicValueMatching.objects.bulk_create(char_value_mathing_list)
