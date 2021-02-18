import json

from django.conf import settings

import redis

DB = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
try:
    assert DB.ping()
except Exception as e:
    if not settings.NO_DB:
        raise e


def is_valid_language(text):
    return not any([c in text for c in "$^[]"])


def is_valid_word(text):
    return not any([c in text for c in "$^[]*"])


def get_cognates(lang, word, *, comparison):
    assert is_valid_language(lang)
    assert is_valid_word(word)
    if comparison == "equal":
        return get_equal_cognates(lang, word)
    else:
        return get_any_cognates(lang, word)


def get_any_cognates(lang, word):
    if lang == "*":
        return get_any_cognates_for_all_languages(word)
    else:
        return get_any_cognates_for_one_language(lang, word)


def get_equal_cognates(lang, word):
    if lang == "*":
        return get_equal_cognates_for_all_languages(word)
    else:
        return get_equal_cognates_for_one_language(lang, word)


async def get_any_cognates_for_all_languages(word):
    cognate_hashes = set()
    for key in DB.keys(f"cognate:*:{word}"):
        for cognate in DB.lrange(key, 0, -1):
            if hash(cognate) in cognate_hashes:
                continue
            cognate_hashes.add(hash(cognate))
            yield json.loads(cognate)


async def get_any_cognates_for_one_language(lang, word):
    for cognate in DB.lrange(f"cognate:{lang}:{word}", 0, -1):
        yield json.loads(cognate)


async def get_equal_cognates_for_all_languages(word):
    async for cognate in get_any_cognates_for_all_languages(word):
        if cognate["word"] == word:
            yield cognate


async def get_equal_cognates_for_one_language(lang, word):
    async for cognate in get_any_cognates_for_one_language(lang, word):
        if cognate["word"] == word:
            yield cognate
