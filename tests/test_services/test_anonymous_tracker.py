import pytest

from core.services.activity_tracking import anonymous_tracker
from core.services.redis import RedisPrefix


@pytest.fixture
def ip(faker) -> str:
    return faker.ipv4()


def test_mark_visitor(ip, redis_test_client):
    anonymous_tracker.mark_visitor(ip)
    key = RedisPrefix.ANONYMOUS.key(ip)
    assert redis_test_client.get(key) == "1"


def test_is_visitor(faker, ip):
    anonymous_tracker.mark_visitor(ip)
    assert anonymous_tracker.is_visitor(ip)
    assert not anonymous_tracker.is_visitor(faker.ipv4())


def test_remove_visitor(ip):
    anonymous_tracker.mark_visitor(ip)
    anonymous_tracker.remove_visitor(ip)
    assert not anonymous_tracker.is_visitor(ip)


def test_get_visitors(faker, ip):
    another_ip = faker.ipv4()
    anonymous_tracker.mark_visitor(ip)
    anonymous_tracker.mark_visitor(another_ip)
    ips = anonymous_tracker.get_visitors()
    assert set(ips) == {ip, another_ip}
    anonymous_tracker.remove_visitor(ip)
    anonymous_tracker.remove_visitor(another_ip)
    assert len(anonymous_tracker.get_visitors()) == 0
