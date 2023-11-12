from django.db.models.signals import (
    post_save,
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


@receiver(post_save, sender=Product)
def product_saved(sender, instance, created, **kwargs):
    if not instance.translated_name:
        translate_product(instance.id, instance.name)
