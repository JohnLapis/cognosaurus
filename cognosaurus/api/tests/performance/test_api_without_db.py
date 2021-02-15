import cProfile

import pytest
from django.conf import settings

settings.NO_DB = True


from rest_framework.test import APIRequestFactory

import cognosaurus.api.views as view_module
from cognosaurus.api.views import CognateSerializer, CognateViewSet, get_cognates

view_module_globals = vars(view_module)
# Mock function that interacts with database
view_module_globals[get_cognates.__name__] = lambda *args, **kwags: (
    {"word": str(i), "lang": "eng"} for i in range(10)
)


@pytest.fixture(scope="module")
def rf():
    yield APIRequestFactory()


def test_cognate_viewset_in_loop(rf):
    paths = [
        "/words?por=deus",
        "/",
        "/words",
        "/words?*=no",
        "/words?eng=banana&comparison=equal",
        "/words?fra=bataillon&por=entidade",
        "/words?fra=ba*&por=entidade",
        "/words?zzzzzzz=zzzz&por=entidade",
    ]
    viewset = CognateViewSet.as_view({"get": "list"})
    print()
    cProfile.runctx(
        "for path in paths: viewset(rf.get(path))",
        view_module_globals,
        locals(),
    )
