from core.utils import get_client_ip


def test_returns_remote_addr(request_builder):
    request = request_builder()
    assert get_client_ip(request) == "127.0.0.1"


def test_prefers_x_forwarded_for(request_builder):
    request = request_builder(HTTP_X_FORWARDED_FOR="1.2.3.4, 5.6.7.8")
    assert get_client_ip(request) == "1.2.3.4"


def test_strips_whitespace_from_x_forwarded_for(request_builder):
    request = request_builder(HTTP_X_FORWARDED_FOR="  1.2.3.4  , 5.6.7.8")
    assert get_client_ip(request) == "1.2.3.4"


def test_returns_empty_string_if_no_ip(request_builder):
    request = request_builder()
    request.META.pop("REMOTE_ADDR", None)
    assert get_client_ip(request) == ""
