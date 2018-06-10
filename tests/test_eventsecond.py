import time
import pytest

from .context import counttracker


def test_init():
    timestamp = time.time()
    es = counttracker.EventSecond(timestamp)

    assert es is not None
    assert isinstance(es.timestamp, int)
    assert es.count == 0


def test_init_fail():
    with pytest.raises(AssertionError):
        es = counttracker.EventSecond("Fail")

    with pytest.raises(AssertionError):
        es = counttracker.EventSecond(1)


def test_log_event():
    timestamp = time.time()
    es = counttracker.EventSecond(timestamp)

    es.log_event()
    assert es.count == 1

    es.log_event()
    assert es.count == 2


def test_eq():
    timestamp = time.time()
    es0 = counttracker.EventSecond(timestamp)
    es1 = counttracker.EventSecond(timestamp)

    assert es0 == es1
    assert es0 is not es1
    assert not(es0 == 0)


def test_ne():
    timestamp = time.time()
    es0 = counttracker.EventSecond(timestamp)
    es1 = counttracker.EventSecond(timestamp+1)

    assert es0 != es1
    assert es0 is not es1


def test_lt():
    timestamp = time.time()
    es0 = counttracker.EventSecond(timestamp)
    es1 = counttracker.EventSecond(timestamp+1)
    es2 = counttracker.EventSecond(timestamp)

    assert es0 < es1
    assert not es0 < es2
    assert not es1 < es2
    assert not (es0 < 0)


def test_le():
    timestamp = time.time()
    es0 = counttracker.EventSecond(timestamp)
    es1 = counttracker.EventSecond(timestamp+1)
    es2 = counttracker.EventSecond(timestamp)

    assert es0 <= es1
    assert es0 <= es2
    assert not es1 <= es2


def test_gt():
    timestamp = time.time()
    es0 = counttracker.EventSecond(timestamp)
    es1 = counttracker.EventSecond(timestamp+1)
    es2 = counttracker.EventSecond(timestamp)

    assert not es0 > es1
    assert not es0 > es2
    assert es1 > es2


def test_ge():
    timestamp = time.time()
    es0 = counttracker.EventSecond(timestamp)
    es1 = counttracker.EventSecond(timestamp+1)
    es2 = counttracker.EventSecond(timestamp)

    assert not es0 >= es1
    assert es0 >= es2
    assert es1 >= es2