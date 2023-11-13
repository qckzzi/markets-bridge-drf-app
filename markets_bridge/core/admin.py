from django.contrib import (
    admin,
)

from core.mixins import (
    ReadOnlyAdminMixin,
)


class ReadOnlyModelAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    pass