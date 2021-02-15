import cProfile

import pytest
from rest_framework.test import APIRequestFactory

from cognosaurus.api.views import CognateViewSet


@pytest.fixture(scope="module")
def rf():
    yield APIRequestFactory()


def _test_cognate_viewset_in_loop(rf):
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
    cProfile.runctx("for path in paths: viewset(rf.get(path))", globals(), locals())


def test_cognate_viewset(rf):
    path = "/words?*=no"
    request = rf.get(path)
    viewset = CognateViewSet.as_view({"get": "list"})
    print()
    cProfile.runctx("viewset(request)", globals(), locals())
