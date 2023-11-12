from django.db.models import (
    QuerySet,
)

from parser_targets.models import (
    RawCategory,
    RawProduct,
)


def get_allowed_products() -> QuerySet[RawProduct]:
    return RawProduct.objects.filter(is_allowed_import=True)


def get_allowed_categories() -> QuerySet[RawCategory]:
    return RawCategory.objects.filter(is_allowed_import=True)
