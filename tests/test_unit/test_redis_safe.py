from redis.exceptions import ConnectionError, RedisError, TimeoutError

from core.services.redis import redis_safe


def test_redis_safe_returns_default_on_connection_error():
    @redis_safe(default=[])
    def failing_func():
        raise ConnectionError

    assert failing_func() == []


def test_redis_safe_returns_default_on_timeout():
    @redis_safe(default=0)
    def failing_func():
        raise TimeoutError

    assert failing_func() == 0


def test_redis_safe_returns_default_on_redis_error():
    @redis_safe(default=None)
    def failing_func():
        raise RedisError

    assert failing_func() is None


def test_redis_safe_returns_value_on_success():
    @redis_safe(default=None)
    def success_func():
        return "ok"

    assert success_func() == "ok"
