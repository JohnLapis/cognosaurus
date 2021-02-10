import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    yield APIClient()


@pytest.mark.parametrize(
    "path,expected",
    [
        # basic requests
        (
            "/words?por=deus",
            {
                "results": {
                    "por:deus": [
                        {
                            "word": "deus",
                            "language": "Latin",
                        }
                    ],
                },
            },
        ),
        ("/", {"words": "http://testserver/words"}),
        ("/words", {"results": {}}),
        # shows how to use wildcards for languages
        (
            "/words?*=no",
            {
                "results": {
                    "*:no": [
                        {"language": "Portuguese", "word": "não"},
                        {"language": "Spanish", "word": "no"},
                        {"language": "Papiamento", "word": "no"},
                        {"language": "Latin", "word": "non"},
                        {"language": "Japanese", "word": "ノー"},
                    ]
                }
            },
        ),
        # shows how to compare cognates exactly
        (
            "/words?eng=banana&comparison=equal",
            {
                "results": {
                    "eng:banana": [
                        {
                            "word": "banana",
                            "language": "Portuguese",
                        },
                        {
                            "word": "banana",
                            "language": "Welsh",
                        },
                        {
                            "word": "banana",
                            "language": "Tok Pisin",
                        },
                    ],
                },
            },
        ),
        # multiple parameters can be passed
        (
            "/words?fra=bataillon&por=entidade",
            {
                "results": {
                    "fra:bataillon": [
                        {
                            "word": "bataillon",
                            "language": "German",
                        },
                        {
                            "word": "battaglione",
                            "language": "Italian",
                        },
                        {
                            "word": "pataljoona",
                            "language": "Finnish",
                        },
                    ],
                    "por:entidade": [
                        {
                            "word": "entitas",
                            "language": "Latin",
                        }
                    ],
                }
            },
        ),
        # wildcards aren't allowed inside words
        (
            "/words?fra=ba*&por=entidade",
            {
                "results": {
                    "fra:ba*": None,
                    "por:entidade": [
                        {
                            "word": "entitas",
                            "language": "Latin",
                        }
                    ],
                }
            },
        ),
        # parameters that aren't valid languages are ignored
        (
            "/words?zzzzzzz=zzzz&por=entidade",
            {
                "results": {
                    "por:entidade": [
                        {
                            "word": "entitas",
                            "language": "Latin",
                        }
                    ],
                }
            },
        ),
    ],
)
def test_cognate_viewset(client, path, expected):
    response = client.get(path)
    assert response.data == expected
