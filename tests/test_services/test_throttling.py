import core.services.throttling.throttling as throttling

KEY = throttling.build_key("test_action", "test_id")


def test_set_throttled_in_redis(redis_test_client):
    throttling.set_throttled(KEY)
    assert redis_test_client.get(KEY) == "1"
    assert throttling.set_throttled(KEY) == 2


def test_set_throttled_set_ttl(redis_test_client):
    throttling.set_throttled(KEY)
    assert redis_test_client.ttl(KEY) > 0


def test_set_throttled_does_not_reset_ttl_on_subsequent_calls(redis_test_client):
    throttling.set_throttled(KEY)
    ttl_after_first = redis_test_client.ttl(KEY)
    throttling.set_throttled(KEY)
    ttl_after_second = redis_test_client.ttl(KEY)
    assert ttl_after_second <= ttl_after_first


def test_exceed_limit_returns_false_below_limit():
    throttling.set_throttled(KEY)
    assert throttling.exceed_limit(KEY, rate_limit=5) is False


def test_exceed_limit_returns_true_above_limit():
    for _ in range(5):
        throttling.set_throttled(KEY)
    assert throttling.exceed_limit(KEY, rate_limit=3) is True


def test_exceed_limit_returns_false_for_missing_key():
    assert throttling.exceed_limit(KEY, rate_limit=10) is False


def test_remove_throttled_deletes_key(redis_test_client):
    throttling.set_throttled(KEY)
    throttling.remove_throttled(KEY)
    assert not redis_test_client.exists(KEY)


def test_is_throttled_returns_false_below_limit():
    assert throttling.is_throttled(KEY, rate_limit=10) is False


def test_is_throttled_returns_true_above_limit():
    for _ in range(5):
        throttling.is_throttled(KEY, rate_limit=3)
    assert throttling.is_throttled(KEY, rate_limit=3) is True
