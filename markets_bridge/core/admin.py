from django.contrib import (
    admin,
)
from django.contrib.admin import (
    SimpleListFilter,
)

from core.mixins import (
    ReadOnlyAdminMixin,
    YerOrNoFilterMixin,
)


class ReadOnlyModelAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    pass


class BaseYesOrNoFilter(YerOrNoFilterMixin, SimpleListFilter):
    pass


class BaseNullFilter(BaseYesOrNoFilter):
    field_name = None

    def queryset(self, request, queryset):
        value = self.value()

        if value is not None:
            value_is_null = value == 'True'
            queryset = queryset.filter(
                **{f'{self.field_name}__isnull': value_is_null},
            )

        return queryset