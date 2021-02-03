from functools import reduce
from itertools import starmap

import iso639
from iso639.exceptions import InvalidLanguageValue
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from cognosaurus.api.models import get_cognates
from cognosaurus.api.serializers import CognateSerializer


class CognateViewSet(ViewSet):
    """Returns cognates for every word in the url query."""

    serializer_class = CognateSerializer

    def list(self, request):
        def get_data(*args):
            return self.get_data(*args)

        data = starmap(get_data, request.query_params.lists())
        data = filter(None, data)
        data = reduce(lambda a, b: {**a, **b}, data, {})
        return Response({"results": data})

    def get_data(self, lang, words):
        try:
            lang_code = iso639.Lang(lang).pt3
        except InvalidLanguageValue:
            return None

        return {word: self.get_cognates(lang_code, word) for word in words}

    def get_cognates(self, lang, word):
        cognates = []
        for cognate in get_cognates(lang, word):
            serializer = self.serializer_class(
                data={
                    "word": cognate["word"],
                    "language": iso639.Lang(cognate["lang"]).name,
                }
            )
            assert serializer.is_valid()
            cognates.append(serializer.data)

        return cognates
