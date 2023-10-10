from django.contrib import admin
from parser_targets.models import (
    RawCategory,
    RawProduct,
)


@admin.register(RawCategory)
class RawCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(RawProduct)
class RawProductAdmin(admin.ModelAdmin):
    pass



