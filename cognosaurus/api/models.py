import json

import redis
from django.conf import settings

DB = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


def get_cognates(lang, word, *, comparison):
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


def get_any_cognates_for_all_languages(word):
    for key in DB.keys(f"cognate:*:{word}"):
        for cognate in DB.lrange(key, 0, -1):
            yield json.loads(cognate)


def get_any_cognates_for_one_language(lang, word):
    for cognate in DB.lrange(f"cognate:{lang}:{word}", 0, -1):
        yield json.loads(cognate)


def get_equal_cognates_for_all_languages(word):
    for key in DB.keys(f"cognate:*:{word}"):
        for cognate in DB.lrange(key, 0, -1):
            cognate = json.loads(cognate)
            if cognate["word"] == word:
                yield cognate


def get_equal_cognates_for_one_language(lang, word):
    for cognate in DB.lrange(f"cognate:{lang}:{word}", 0, -1):
        cognate = json.loads(cognate)
        if cognate["word"] == word:
            yield cognate
