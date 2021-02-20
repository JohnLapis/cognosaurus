import cProfile
import os

from rest_framework.test import RequestsClient


def test_cognate_viewset_in_loop():
    with open(os.path.dirname(__file__) + "/code_for_e2e_test.py", "r") as f:
        code = f.read()
    client = RequestsClient()
    print()
    cProfile.runctx(code, globals(), locals())
