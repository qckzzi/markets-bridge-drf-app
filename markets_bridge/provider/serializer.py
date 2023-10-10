from rest_framework.serializers import ModelSerializer

from provider.models import ScrappedProduct

class ScrappedProductSerializer(ModelSerializer):
    class Meta:
        model = ScrappedProduct
        fields = '__all__'
