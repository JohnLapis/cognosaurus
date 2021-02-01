from rest_framework import serializers


class CognateSerializer(serializers.Serializer):
    cognate = serializers.CharField(max_length=80)
    language = serializers.CharField(max_length=60)
