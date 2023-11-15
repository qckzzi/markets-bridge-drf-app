from rest_framework.serializers import (
    ModelSerializer,
)

from common.models import (
    Log,
    SystemEnvironment,
)


class SystemEnvironmentSerializer(ModelSerializer):
    class Meta:
        model = SystemEnvironment
        fields = '__all__'


class LogSerializer(ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'