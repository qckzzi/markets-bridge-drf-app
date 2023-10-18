from rest_framework.serializers import (
    ModelSerializer,
)

from recipient.models import (
    RecipientCategory,
    RecipientCharacteristic,
    RecipientCharacteristicValue,
)


class RecipientCategorySerializer(ModelSerializer):
    class Meta:
        model = RecipientCategory
        fields = '__all__'


class RecipientCharacteristicSerializer(ModelSerializer):
    class Meta:
        model = RecipientCharacteristic
        fields = '__all__'


class RecipientCharacteristicValueSerializer(ModelSerializer):
    class Meta:
        model = RecipientCharacteristicValue
        fields = '__all__'
