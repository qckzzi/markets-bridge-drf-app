from django.db.models import (
    Q,
)
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
)
from common.services import (
    create_product_type_characteristic_matching,
    get_recipient_category_id_by_category_mathing_id,
)
from core.constants import (
    PRODUCT_TYPE_CHARACTERISTIC_EXTERNAL_ID,
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
            create_product_type_characteristic_matching(instance.id)


@receiver(pre_save, sender=CharacteristicMatching)
def category_matching_pre_saved(sender, instance, *args, **kwargs):
    """Кеширует данные перед сохранением."""

    characteristic_external_id = instance.recipient_characteristic.characteristic.external_id

    if characteristic_external_id == PRODUCT_TYPE_CHARACTERISTIC_EXTERNAL_ID and instance.recipient_value:
        instance.__original_recipient_value_id = CharacteristicMatching.objects.get(id=instance.id).recipient_value_id


@receiver(post_save, sender=CharacteristicMatching)
def characteristic_matching_saved(sender, instance, created, **kwargs):
    """Производит действия после сохранения записи сопоставления характеристики."""

    # FIXME: Место прибито гвоздями.
    #        Эта проверка захардкожена, т.к. пока не найдено решение того,
    #        как идентифицировать тип товара озона (по факту это характеристика).
    characteristic_external_id = instance.recipient_characteristic.characteristic.external_id

    if characteristic_external_id == PRODUCT_TYPE_CHARACTERISTIC_EXTERNAL_ID and instance.recipient_value:
        if instance.__original_recipient_value_id != instance.recipient_value_id:
            CharacteristicMatching.objects.filter(
                Q(category_matching_id=instance.category_matching_id),
                ~Q(id=instance.id),
            ).delete()

        update_recipient_attributes(
            instance.category_matching.recipient_category.external_id,
            instance.recipient_value.external_id,
            instance.category_matching_id
        )
