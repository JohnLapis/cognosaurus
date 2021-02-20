import cProfile
import inspect
import os

import pytest
from django.conf import settings

settings.NO_DB = True


from rest_framework.test import APIRequestFactory

import cognosaurus.api.views as view_module
from cognosaurus.api.views import CognateSerializer, CognateViewSet, get_cognates

view_module_globals = vars(view_module)
# Mock function that interacts with database
async def mockGetCognates(*args, **kwargs):
    for i in range(10):
        yield {"word": str(i), "lang": "eng"}


view_module_globals[get_cognates.__name__] = mockGetCognates


def test_cognate_viewset_in_loop():
    rf = APIRequestFactory()
    with open(os.path.dirname(__file__) + "/code_for_test_big_request.py", "r") as f:
        code = f.read()
    print()
    cProfile.runctx(code, globals(), locals())
