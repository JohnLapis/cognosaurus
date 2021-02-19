from functools import reduce
from itertools import starmap

import iso639
from asgiref.sync import async_to_sync
from iso639.exceptions import InvalidLanguageValue
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from cognosaurus.api.models import get_cognates, is_valid_word
from cognosaurus.api.serializers import CognateSerializer


class CognateViewSet(ViewSet):
    """Returns cognates for every word in the url query."""

    serializer_class = CognateSerializer

    def list(self, request):
        params = {
            "comparison": request.query_params.get("comparison"),
        }

        @async_to_sync
        async def _get_data(*args):
            return await self.get_data(*args, **params)

        data = starmap(_get_data, request.query_params.lists())
        data = filter(None, data)
        data = reduce(lambda a, b: {**a, **b}, data, {})
        return Response({"results": data})

    async def get_data(self, lang, words, **params):
        if lang != "*":
            try:
                lang = iso639.Lang(lang).pt3
            except InvalidLanguageValue:
                return None

        data = {}
        for word in words:
            data[f"{lang}:{word}"] = await self.get_cognates(lang, word, **params)

        return data

    async def get_cognates(self, lang, word, **params):
        cognates = []
        if not is_valid_word(word):
            return None
        async for cognate in get_cognates(lang, word, **params):
            serializer = self.serializer_class(
                data={
                    "word": cognate["word"],
                    "language": iso639.Lang(cognate["lang"]).name,
                }
            )
            assert serializer.is_valid()
            cognates.append(serializer.data)

        return cognates
