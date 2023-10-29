from django.db.models import (
    F,
    QuerySet,
)
from django.http import (
    Http404,
)
from rest_framework.generics import (
    get_object_or_404,
)

from recipient.models import (
    Category,
    Characteristic,
    CharacteristicValue,
)


def update_or_create_category(category_data: dict) -> tuple[Category, bool]:
    """Создаёт новую категорию, либо обновляет связь с ее родителями."""

    external_id = category_data.get('external_id')
    parent_category_external_ids = category_data.pop('parent_category_external_ids')
    marketplace_id = category_data.get('marketplace_id')

    category, is_new = Category.objects.get_or_create(
        external_id=external_id,
        marketplace_id=marketplace_id,
        defaults=category_data,
    )

    if parent_category_external_ids:
        parent_categories = Category.objects.filter(
            external_id__in=parent_category_external_ids,
            marketplace_id=marketplace_id,
        )

        if is_new:
            category.parent_categories.set(parent_categories)
        else:
            for parent_category in parent_categories:
                category.parent_categories.add(parent_category)

    return category, is_new


def update_or_create_characteristic(characteristic_data: dict) -> tuple[Characteristic, bool]:
    """Создает новую характеристику, либо обновляет ее связи с категориями."""

    external_id = characteristic_data.get('external_id')
    category_external_ids = characteristic_data.pop('category_external_ids')
    marketplace_id = characteristic_data.pop('marketplace_id')

    characteristic, is_new = Characteristic.objects.get_or_create(
        external_id=external_id,
        categories__marketplace_id=marketplace_id,
        defaults=characteristic_data,
    )

    categories = Category.objects.filter(
        external_id__in=category_external_ids,
        marketplace_id=marketplace_id,
    )

    if is_new:
        characteristic.categories.set(categories)
    else:
        characteristic.categories.add(*categories)

    return characteristic, is_new


def update_or_create_characteristic_value(value_data: dict) -> tuple[CharacteristicValue, bool]:
    """Создает новое значение характеристики, либо обновляет его."""

    external_id = value_data.get('external_id')
    characteristic_external_id = value_data.pop('characteristic_external_id')
    marketplace_id = value_data.pop('marketplace_id')

    # TODO: Использовать get_object_or_404
    characteristic = Characteristic.objects.filter(
        external_id=characteristic_external_id,
        categories__marketplace_id=marketplace_id,
    ).distinct()

    if not characteristic.exists():
        raise Http404('Characteristic not found')

    value_data['characteristic_id'] = characteristic.get().id

    characteristic_value, is_new = CharacteristicValue.objects.get_or_create(
        external_id=external_id,
        characteristic__categories__marketplace_id=marketplace_id,
        defaults=value_data,
    )

    return characteristic_value, is_new


def get_matched_categories() -> QuerySet[Category]:
    """Возвращает категории получателя, сопоставленные с категориями поставщика."""

    categories = Category.objects.filter(
        provider_categories__isnull=False,
    ).values(
        'external_id',
        parent_external_id=F('parent_categories__external_id'),
    )

    return categories
