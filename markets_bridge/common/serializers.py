from rest_framework import (
    fields,
)
from rest_framework.serializers import (
    ALL_FIELDS,
    ModelSerializer,
    Serializer,
)

from common.models import (
    Log,
    SystemVariable,
)


class SystemVariableSerializer(ModelSerializer):
    class Meta:
        model = SystemVariable
        fields = ALL_FIELDS


class LogSerializer(ModelSerializer):
    class Meta:
        model = Log
        fields = ALL_FIELDS


class CharacteristicMatchingSerializer(Serializer):
    category_matching_id = fields.IntegerField(
        required=True,
        label='Идентификатор сопоставления категории',
    )