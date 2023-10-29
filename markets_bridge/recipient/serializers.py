from rest_framework.fields import (
    IntegerField,
)
from rest_framework.serializers import (
    ALL_FIELDS,
    ModelSerializer,
    Serializer,
)

from recipient.models import (
    Category,
    Characteristic,
    CharacteristicValue,
)


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ALL_FIELDS


class RelevantCategorySerializer(Serializer):
    external_id = IntegerField()
    parent_external_id = IntegerField()


class CharacteristicSerializer(ModelSerializer):
    class Meta:
        model = Characteristic
        fields = ALL_FIELDS


class CharacteristicValueSerializer(ModelSerializer):
    class Meta:
        model = CharacteristicValue
        fields = ALL_FIELDS
