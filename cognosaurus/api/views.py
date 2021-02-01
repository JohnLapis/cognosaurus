from functools import reduce
from itertools import starmap

import iso639
from iso639.exceptions import InvalidLanguageValue
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from cognosaurus.api.serializers import CognateSerializer
from cognosaurus.api.models import Cognate
from django.db.models import Q


class CognateViewSet(ViewSet):
    queryset = Cognate.objects.all()

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
        results = self.queryset.filter(
            Q(word_1__eq=word, lang_1__eq=lang) | word_2__eq=word, lang_2__eq=lang
        ).values("word_1", "lang_1", "word_2", "lang_2")

        data = []
        for result in results:
            column_suffix = "2" if lang == result.lang_1 else "1"
            cognate = getattr(result, f"word_{column_suffix}")
            cognate_lang = getattr(result, f"lang_{column_suffix}")
            data.append({
                "cognate": cognate,
                "language": iso639.Lang(cognate_lang).name
            })

        serializer = CognateSerializer(data=data, many=True)
        assert serializer.is_valid()
        return serializer.data
