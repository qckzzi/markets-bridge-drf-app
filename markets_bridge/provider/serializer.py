from rest_framework.serializers import (
    ModelSerializer,
)

from provider.models import (
    ProductImage,
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
