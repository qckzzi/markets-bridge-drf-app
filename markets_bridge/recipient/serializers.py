from rest_framework.serializers import (
    ALL_FIELDS,
    ModelSerializer,
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
        ref_name = 'RecipientCategory'


class CharacteristicSerializer(ModelSerializer):
    class Meta:
        model = Characteristic
        fields = ALL_FIELDS
        ref_name = 'RecipientCharacteristic'


class CharacteristicValueSerializer(ModelSerializer):
    class Meta:
        model = CharacteristicValue
        fields = ALL_FIELDS
        ref_name = 'RecipientCharacteristicValue'
