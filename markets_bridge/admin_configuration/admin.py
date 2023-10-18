from django.contrib import (
    admin,
)

from admin_configuration.mixins import (
    ReadOnlyAdminMixin,
)


admin.site.site_title = 'Markets bridge'
admin.site.site_header = 'Markets bridge'
admin.site.index_title = 'Администрирование'

class ReadOnlyModelAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    pass
