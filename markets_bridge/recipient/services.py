from django.db.models import (
    QuerySet,
)
from django.db.transaction import (
    atomic,
)
from rest_framework.generics import (
    get_object_or_404,
)

from recipient.models import (
    Category,
    Characteristic,
    CharacteristicForCategory,
    CharacteristicValue,
)


@atomic
def update_or_create_category(category_data: dict) -> tuple[Category, bool]:
    """Создаёт новую категорию, либо обновляет связь с ее родителем."""

    external_id = category_data.get('external_id')
    parent_category_external_id = category_data.pop('parent_category_external_id')
    marketplace_id = category_data.get('marketplace_id')

    category, is_new = Category.objects.get_or_create(
        external_id=external_id,
        marketplace_id=marketplace_id,
        defaults=category_data,
    )

    try:
        parent_category = Category.objects.get(
            external_id=parent_category_external_id,
            marketplace_id=marketplace_id,
        )
    except Category.DoesNotExist:
        parent_category = None

    category.parent_category = parent_category

    category.save()

    return category, is_new


def update_or_create_characteristic(characteristic_data: dict) -> tuple[Characteristic, bool]:
    """Создает новую характеристику, либо обновляет ее связи с категориями."""

    external_id = characteristic_data.get('external_id')
    category_external_id = characteristic_data.pop('category_external_id')
    marketplace_id = characteristic_data.get('marketplace_id')
    is_required_characteristic = characteristic_data.pop('is_required')

    characteristic, is_new = Characteristic.objects.get_or_create(
        external_id=external_id,
        marketplace_id=marketplace_id,
        defaults=characteristic_data,
    )

    category = Category.objects.get(
        external_id=category_external_id,
        marketplace_id=marketplace_id,
    )

    CharacteristicForCategory.objects.get_or_create(
        category=category,
        characteristic=characteristic,
        defaults={'is_required': is_required_characteristic},
    )

    return characteristic, is_new


def update_or_create_characteristic_value(value_data: dict) -> tuple[CharacteristicValue, bool]:
    """Создает новое значение характеристики, либо обновляет его."""

    external_id = value_data.get('external_id')
    characteristic_external_id = value_data.pop('characteristic_external_id')
    marketplace_id = value_data.get('marketplace_id')

    characteristic = get_object_or_404(
        Characteristic,
        external_id=characteristic_external_id,
        marketplace_id=marketplace_id,
    )

    value_data['characteristic_id'] = characteristic.id

    characteristic_value, is_new = CharacteristicValue.objects.get_or_create(
        external_id=external_id,
        marketplace_id=marketplace_id,
        defaults=value_data,
    )

    return characteristic_value, is_new


def get_matched_category_external_ids() -> QuerySet[int]:
    """Возвращает категории получателя, сопоставленные с категориями поставщика."""

    categories = Category.objects.filter(
        matchings__isnull=False,
    ).values_list(
        'external_id',
        flat=True,
    ).distinct()

    return categories
