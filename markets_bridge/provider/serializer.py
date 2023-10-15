from rest_framework.serializers import (
    ModelSerializer,
)

from provider.models import (
    ProductCharacteristicValue,
    ProductImage,
    ProviderCategory,
    ProviderCharacteristic,
    ProviderCharacteristicValue,
    ScrappedProduct,
)


class ScrappedProductSerializer(ModelSerializer):
    class Meta:
        model = ScrappedProduct
        fields = '__all__'


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProviderCategorySerializer(ModelSerializer):
    class Meta:
        model = ProviderCategory
        fields = '__all__'


class ProviderCharacteristicSerializer(ModelSerializer):
    class Meta:
        model = ProviderCharacteristic
        fields = '__all__'


class ProviderCharacteristicValueSerializer(ModelSerializer):
    class Meta:
        model = ProviderCharacteristicValue
        fields = '__all__'


class ProductCharacteristicValueSerializer(ModelSerializer):
    class Meta:
        model = ProductCharacteristicValue
        fields = '__all__'
        
