from rest_framework.serializers import (
    ALL_FIELDS,
    ModelSerializer,
)

from provider.models import (
    Brand,
    Category,
    Characteristic,
    CharacteristicValue,
    Product,
    ProductImage,
)


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ALL_FIELDS


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ALL_FIELDS


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ALL_FIELDS
        ref_name = 'ProviderCategory'


class CharacteristicSerializer(ModelSerializer):
    class Meta:
        model = Characteristic
        fields = ALL_FIELDS
        ref_name = 'ProviderCharacteristic'


class CharacteristicValueSerializer(ModelSerializer):
    class Meta:
        model = CharacteristicValue
        fields = ALL_FIELDS
        ref_name = 'ProviderCharacteristicValue'


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ALL_FIELDS
