from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from cognosaurus.api.serializers import CognateSerializer

LANGUAGES = ["en", "int", "jp", "pt-br", "ru"]


class CognateViewSet(ViewSet):
    def get_queryset(self, word, lang):
        return [{"cognate": word, "language": lang}]

    def list(self, request):
        results = {}
        for lang, words in request.query_params.lists():
            for word in words:
                if lang not in LANGUAGES and False:
                    continue
                queryset = self.get_queryset(word, lang)
                serializer = CognateSerializer(data=queryset, many=True)
                assert serializer.is_valid()
                results[word] = serializer.data

        return Response({"results": results})
