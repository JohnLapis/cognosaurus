import cProfile
import inspect
import os

import pytest
from rest_framework.test import APIRequestFactory

from cognosaurus.api.views import CognateViewSet


@pytest.fixture(scope="module")
def rf():
    yield APIRequestFactory()


def test_cognate_viewset_in_loop():
    viewset = CognateViewSet.as_view({"get": "list"})
    with open(os.path.dirname(__file__) + "/code_for_test.py", "r") as f:
        code = f.read()
    print()
    cProfile.runctx(code, globals(), locals())
