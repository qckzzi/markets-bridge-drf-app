from rest_framework.serializers import (
    ModelSerializer,
)

from common.models import (
    Log,
    SystemVariable,
)


class SystemVariableSerializer(ModelSerializer):
    class Meta:
        model = SystemVariable
        fields = '__all__'


class LogSerializer(ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'