import os

import pytest
import requests

HOST = os.environ["HOST"]
PORT = os.environ["PORT"]


def get_language(d):
    return d["language"]


def compare_results(results, expected_results):
    assert set(results.keys()) == set(expected_results.keys())
    for result in zip(results.values(), expected_results.values()):
        cognates, expected_cognates = result
        if isinstance(expected_cognates, list):
            cognates = sorted(cognates, key=get_language)
            expected_cognates = sorted(expected_cognates, key=get_language)
            assert cognates == expected_cognates
        else:
            assert cognates == expected_cognates


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
        ("/", {"words": f"http://{HOST}:{PORT}/words"}),
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
def test_cognate_viewset(path, expected):
    response = requests.get(f"http://{HOST}:{PORT}{path}")

    assert response.status_code == 200

    data = response.json()
    if "results" in expected:
        compare_results(data["results"], expected["results"])
        data["results"] = None
        expected["results"] = None

    assert data == expected
