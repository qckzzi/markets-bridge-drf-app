from django.contrib import (
    admin,
)
from django.contrib.admin.sites import (
    site,
)
from django.contrib.admin.widgets import (
    ForeignKeyRawIdWidget,
)

from common.models import (
    Currency,
)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


# @admin.register(CategoryMatching)
# class CategoryMatchingAdmin(admin.ModelAdmin):
#     raw_id_fields = ('provider_category', 'recipient_category')
