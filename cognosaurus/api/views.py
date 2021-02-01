from functools import reduce
from itertools import starmap

import iso639
from iso639.exceptions import InvalidLanguageValue
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from cognosaurus.api.serializers import CognateSerializer


class CognateViewSet(ViewSet):
    def list(self, request):
        def get_data(*args):
            return self.get_data(*args)

        data = starmap(get_data, request.query_params.lists())
        data = filter(None, data)
        data = reduce(lambda a, b: {**a, **b}, data, {})
        return Response({"results": data})

    def get_data(self, lang, words):
        try:
            lang = iso639.Lang(lang)
        except InvalidLanguageValue:
            return None

        return {word: self.get_cognates(lang.name, word) for word in words}

    def get_cognates(self, lang, word):
        queryset = self.get_queryset(lang, word)
        serializer = CognateSerializer(data=queryset, many=True)
        assert serializer.is_valid()
        return serializer.data

    def get_queryset(self, lang, word):
        return [{"cognate": word, "language": lang}]
