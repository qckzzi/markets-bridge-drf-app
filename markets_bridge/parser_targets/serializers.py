from rest_framework.serializers import ModelSerializer

from parser_targets.models import RawCategory, RawProduct


class RawCategorySerializer(ModelSerializer):
    class Meta:
        model = RawCategory
        fields = '__all__'


class RawProductSerializer(ModelSerializer):
    class Meta:
        model = RawProduct
        fields = '__all__'