from rest_framework import serializers


class CognateSerializer(serializers.Serializer):
    # make sure it is unicode and verify if 30 is a good limit
    # how to account for whitespace and punctuation?
    # how to make it international too?
    # should i use a regex??
    cognate = serializers.CharField(max_length=30)
    language = serializers.CharField(max_length=30)
