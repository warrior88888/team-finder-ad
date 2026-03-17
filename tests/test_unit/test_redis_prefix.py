from core.services.redis import RedisPrefix, ThrottleAction


def test_key_format():
    assert RedisPrefix.ONLINE.key("123") == "online:123"


def test_key_format_multiple_parts():
    assert (
        RedisPrefix.THROTTLE.key("login_fail", "user@mail.com", "127.0.0.1")
        == "throttle:login_fail:user@mail.com:127.0.0.1"
    )


def test_pattern():
    assert RedisPrefix.ANONYMOUS.pattern() == "anon_visitor:*"


def test_extract_id():
    assert RedisPrefix.ONLINE.extract_id("online:123") == "123"


def test_extract_id_after_action():
    key = RedisPrefix.THROTTLE.key(ThrottleAction.LOGIN_FAIL, "user@mail.com")
    assert (
        RedisPrefix.THROTTLE.extract_id_after_action(key, ThrottleAction.LOGIN_FAIL)
        == "user@mail.com"
    )
