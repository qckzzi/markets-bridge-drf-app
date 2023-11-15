from django.contrib import (
    admin,
)

from parser_targets.models import (
    RawCategory,
    RawProduct,
)


@admin.register(RawCategory)
class RawCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_allowed_import',
        'marketplace',
    )
    list_editable = (
        'is_allowed_import',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'is_allowed_import',
    )


@admin.register(RawProduct)
class RawProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_allowed_import',
        'marketplace',
    )
    list_editable = (
        'is_allowed_import',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'is_allowed_import',
    )
