import asyncio
import json

import aioredis
from django.conf import settings


async def get_db():
    try:
        db = await aioredis.create_redis(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
        )

        assert await db.ping()
        return db
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
    db = await get_db()
    cognate_hashes = set()
    for key in await db.keys(f"cognate:*:{word}"):
        for cognate in await db.lrange(key, 0, -1):
            if hash(cognate) in cognate_hashes:
                continue
            cognate_hashes.add(hash(cognate))
            yield json.loads(cognate)


async def get_any_cognates_for_one_language(lang, word):
    db = await get_db()
    for cognate in await db.lrange(f"cognate:{lang}:{word}", 0, -1):
        yield json.loads(cognate)


async def get_equal_cognates_for_all_languages(word):
    async for cognate in get_any_cognates_for_all_languages(word):
        if cognate["word"] == word:
            yield cognate


async def get_equal_cognates_for_one_language(lang, word):
    async for cognate in get_any_cognates_for_one_language(lang, word):
        if cognate["word"] == word:
            yield cognate
