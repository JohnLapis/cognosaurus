import pytest
import redis
from django.conf import settings


@pytest.fixture
def db():
    return redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


# @st.sth(
#     st.str,
#     st.str,
#     st.list(st.str, min_length=1),
# )
# def test_get_cognates_given_any_string(db, lang, word, list_values, expected):
#     # %sketch
#     # this code tests primarily if function can handle unicode since there's
#     # json deserialization

#     # list_values = ["foo", "bar", "baz"]
#     db.rpush(f"cognate:test:{lang}:{word}", *list_values)
#     assert list(get_cognates(lang, word)) == list_values
