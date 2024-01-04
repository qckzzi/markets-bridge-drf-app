from django.db.models.signals import (
    post_save,
    pre_save,
)
from django.dispatch import (
    receiver,
)

from provider.models import (
    Category,
    Characteristic,
    CharacteristicValue,
    Product,
)
from provider.services import (
    create_category_matching,
)
from provider.utils import (
    translate_category,
    translate_characteristic,
    translate_characteristic_value,
    translate_product,
    translate_product_description,
    update_product,
)


@receiver(post_save, sender=Category)
def category_saved(sender, instance, created, **kwargs):
    if created:
        create_category_matching(category_id=instance.pk)

    if not instance.translated_name:
        translate_category(instance.id, instance.name)


@receiver(post_save, sender=Characteristic)
def characteristic_saved(sender, instance, created, **kwargs):
    if not instance.translated_name:
        translate_characteristic(instance.id, instance.name)


@receiver(post_save, sender=CharacteristicValue)
def characteristic_value_saved(sender, instance, created, **kwargs):
    if not instance.translated_value:
        translate_characteristic_value(instance.id, instance.value)


@receiver(pre_save, sender=Product)
def before_product_saved(sender, instance: Product, *args, **kwargs):
    is_need_update_in_recipient_system = False
    is_need_difference_check = bool(instance.pk and instance.warehouse and instance.upload_date)

    if is_need_difference_check:
        fields_to_check_coincidence = (
            'translated_name',
            'weight',
            'height',
            'depth',
            'width',
        )

        original_product = Product.objects.only(
            *fields_to_check_coincidence,
        ).get(
            pk=instance.pk,
        )

        coincidences = [getattr(instance, x) == getattr(original_product, x) for x in fields_to_check_coincidence]

        if not all(coincidences):
            is_need_update_in_recipient_system = True

    instance.__is_need_update_in_recipient_system = is_need_update_in_recipient_system


@receiver(post_save, sender=Product)
def product_saved(sender, instance, created, **kwargs):
    if instance.name and not instance.translated_name:
        translate_product(instance.id, instance.name)

    if instance.description and not instance.translated_description:
        translate_product_description(instance.id, instance.description)

    if getattr(instance, '__is_need_update_in_recipient_system', False):
        update_product(instance)
