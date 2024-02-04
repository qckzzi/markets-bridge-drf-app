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


@receiver(post_save, sender=CharacteristicMatching)
def characteristic_matching_saved(sender, instance, created, **kwargs):
    """Производит действия после сохранения записи сопоставления характеристики."""

    # FIXME: Место прибито гвоздями.
    #        Эта проверка захардкожена, т.к. пока не найдено решение того,
    #        как идентифицировать тип товара озона (по факту это характеристика).
    product_type_characteristic_id = 8229

    if instance.recipient_characteristic.external_id == product_type_characteristic_id and instance.recipient_value:
        update_recipient_attributes(
            instance.category_matching.recipient_category.external_id,
            instance.recipient_value.external_id,
            instance.category_matching_id
        )
