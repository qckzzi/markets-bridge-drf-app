from rest_framework.serializers import (
    ModelSerializer,
)

from provider.models import (
    Category,
    Characteristic,
    CharacteristicValue,
    Product,
    ProductImage,
)


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CharacteristicSerializer(ModelSerializer):
    class Meta:
        model = Characteristic
        fields = '__all__'


class CharacteristicValueSerializer(ModelSerializer):
    class Meta:
        model = CharacteristicValue
        fields = '__all__'
