class OnlyExternalIdMixin:
    def list(self, request, *args, **kwargs):
        only_need_external_id = request.query_params.get('only_need_external_id', '').lower()

        if only_need_external_id == 'true':
            self.serializer_class.Meta.fields = ('external_id',)

        return super().list(request, *args, **kwargs)
