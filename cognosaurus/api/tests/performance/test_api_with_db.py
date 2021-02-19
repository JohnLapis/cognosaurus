import cProfile
import inspect
import os

import pytest
from rest_framework.test import APIRequestFactory

from cognosaurus.api.views import CognateViewSet


def test_cognate_viewset_in_loop():
    rf = APIRequestFactory()
    with open(os.path.dirname(__file__) + "/code_for_test.py", "r") as f:
        code = f.read()
    print()
    cProfile.runctx(code, globals(), locals())
