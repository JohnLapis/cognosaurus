import inspect
import json

import pytest
from hypothesis import given
from hypothesis import strategies as st

from cognosaurus.api.models import DB as db
from cognosaurus.api.models import (
    get_any_cognates,
    get_any_cognates_for_all_languages,
    get_any_cognates_for_one_language,
    get_cognates,
    get_equal_cognates,
    get_equal_cognates_for_all_languages,
    get_equal_cognates_for_one_language,
    is_valid_language,
    is_valid_word,
)


def cognate(word, lang):
    return json.dumps({"language": lang, "word": word})


@given(st.from_regex(r"[\$\^\[\]]"))
def test_is_valid_language(text):
    assert not is_valid_language(text)


@given(st.from_regex(r"[\$\^\[\]\*]"))
def test_is_valid_word(text):
    assert not is_valid_word(text)


@pytest.mark.parametrize(
    "args,kwargs,expected",
    [
        (
            ["*", "word"],
            {"comparison": None},
            "get_any_cognates_for_all_languages",
        ),
        (
            ["lang", "word"],
            {"comparison": None},
            "get_any_cognates_for_one_language",
        ),
        (
            ["*", "word"],
            {"comparison": "equal"},
            "get_equal_cognates_for_all_languages",
        ),
        (
            ["lang", "word"],
            {"comparison": "equal"},
            "get_equal_cognates_for_one_language",
        ),
    ],
)
def test_get_cognates(args, kwargs, expected):
    generator = get_cognates(*args, **kwargs)
    assert inspect.getframeinfo(generator.gi_frame).function == expected


def test_get_cognates_given_invalid_word():
    with pytest.raises(AssertionError):
        get_cognates("language", "word*", comparison=None)


def test_get_cognates_given_invalid_language():
    with pytest.raises(AssertionError):
        get_cognates("^language", "word", comparison="equal")


@pytest.mark.parametrize(
    "args,kwargs,expected",
    [
        (["*", "word"], {}, "get_any_cognates_for_all_languages"),
        (["lang", "word"], {}, "get_any_cognates_for_one_language"),
    ],
)
def test_get_any_cognates(args, kwargs, expected):
    generator = get_any_cognates(*args, **kwargs)
    assert inspect.getframeinfo(generator.gi_frame).function == expected


@pytest.mark.parametrize(
    "args,kwargs,expected",
    [
        (["*", "word"], {}, "get_equal_cognates_for_all_languages"),
        (["lang", "word"], {}, "get_equal_cognates_for_one_language"),
    ],
)
def test_get_equal_cognates(args, kwargs, expected):
    generator = get_equal_cognates(*args, **kwargs)
    assert inspect.getframeinfo(generator.gi_frame).function == expected


def test_get_any_cognates_for_all_languages():
    word = "bar"

    lang1 = "test:lang1"
    key1 = f"cognate:{lang1}:{word}"
    inserted_cognates_lang1 = [cognate("foo", "foo")]
    db.rpush(key1, *inserted_cognates_lang1)

    lang2 = "test:lang2"
    key2 = f"cognate:{lang2}:{word}"
    inserted_cognates_lang2 = [cognate("foo", "foo"), cognate("zoo", "zoo")]
    db.rpush(key2, *inserted_cognates_lang2)

    cognates = [json.dumps(c) for c in get_any_cognates_for_all_languages(word)]
    db.delete(key1, key2)

    # repeated cognates are filtered out
    assert set(cognates) == set(inserted_cognates_lang1 + inserted_cognates_lang2)


def test_get_any_cognates_for_one_language():
    lang, word = "test:lang", "bar"
    key = f"cognate:{lang}:{word}"
    inserted_cognates = [
        cognate("a", "a"),
        cognate("bar", "b"),
    ]
    db.rpush(key, *inserted_cognates)

    cognates = [json.dumps(c) for c in get_any_cognates_for_one_language(lang, word)]
    db.delete(key)

    assert cognates == inserted_cognates


def test_get_equal_cognates_for_all_languages():
    word = "bar"

    lang1 = "test:lang1"
    key1 = f"cognate:{lang1}:{word}"
    db.rpush(key1, cognate("bar", "b"), cognate("a", "a"))

    lang2 = "test:lang2"
    key2 = f"cognate:{lang2}:{word}"
    db.rpush(key2, cognate("bar", "b"), cognate("bar", "z"), cognate("z", "z"))

    cognates = [json.dumps(c) for c in get_equal_cognates_for_all_languages(word)]
    db.delete(key1, key2)

    # repeated cognates are filtered out
    expected_cognates = [
        cognate("bar", "b"),
        cognate("bar", "z"),
    ]
    assert cognates == expected_cognates


def test_get_equal_cognates_for_one_language():
    lang, word = "test:lang", "bar"
    key = f"cognate:{lang}:{word}"
    inserted_cognates = [
        cognate("a", "a"),
        cognate("bar", "b"),
    ]
    db.rpush(key, *inserted_cognates)

    cognates = [
        json.dumps(c) for c in get_equal_cognates_for_one_language(lang, word)
    ]
    db.delete(key)

    assert cognates == [cognate("bar", "b")]
