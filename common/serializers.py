from rest_framework import serializers


class HealthCheckSerializer(serializers.Serializer):
    DATABASE = 0
    API_INTEGRATION = 1
    COMPONENT_CHOICES=((DATABASE,"database"),(API_INTEGRATION,"Api Integration"))

    component = serializers.ChoiceField(choices=COMPONENT_CHOICES)
