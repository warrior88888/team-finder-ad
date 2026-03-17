import logging

import pytest

from core.services.log.filters import InfoOnlyFilter, WarningAndAboveFilter


@pytest.fixture
def make_record():
    def _make(level: int) -> logging.LogRecord:
        return logging.LogRecord(
            name="test",
            level=level,
            pathname="",
            lineno=0,
            msg="test",
            args=(),
            exc_info=None,
        )

    return _make


def test_info_only_passes_debug(make_record):
    assert InfoOnlyFilter().filter(make_record(logging.DEBUG)) is True


def test_info_only_passes_info(make_record):
    assert InfoOnlyFilter().filter(make_record(logging.INFO)) is True


def test_info_only_blocks_warning(make_record):
    assert InfoOnlyFilter().filter(make_record(logging.WARNING)) is False


def test_info_only_blocks_error(make_record):
    assert InfoOnlyFilter().filter(make_record(logging.ERROR)) is False


def test_info_only_blocks_critical(make_record):
    assert InfoOnlyFilter().filter(make_record(logging.CRITICAL)) is False


def test_warning_and_above_blocks_debug(make_record):
    assert WarningAndAboveFilter().filter(make_record(logging.DEBUG)) is False


def test_warning_and_above_blocks_info(make_record):
    assert WarningAndAboveFilter().filter(make_record(logging.INFO)) is False


def test_warning_and_above_passes_warning(make_record):
    assert WarningAndAboveFilter().filter(make_record(logging.WARNING)) is True


def test_warning_and_above_passes_error(make_record):
    assert WarningAndAboveFilter().filter(make_record(logging.ERROR)) is True


def test_warning_and_above_passes_critical(make_record):
    assert WarningAndAboveFilter().filter(make_record(logging.CRITICAL)) is True
