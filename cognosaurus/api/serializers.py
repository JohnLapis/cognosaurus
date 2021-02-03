from rest_framework import serializers


class CognateSerializer(serializers.Serializer):
    word = serializers.CharField(max_length=80)
    language = serializers.CharField(max_length=60)
