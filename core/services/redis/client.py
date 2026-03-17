import redis

from config import app_config


def make_client() -> redis.Redis:
    return redis.from_url(app_config.redis.url, decode_responses=True)


redis_client = make_client()
