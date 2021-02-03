import redis
import json

from django.db import models
from django.conf import settings


DB = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


def get_cognates(lang, word):
    for cognate in DB.lrange(f"cognate:{lang}:{word}", 0, -1):
        yield json.loads(cognate)
