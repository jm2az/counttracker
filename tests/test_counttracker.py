import time
import pytest

from .context import counttracker


def test_init():
    tracker = counttracker.CountTracker()
    assert tracker is not None


### Test _remove_old_events ###
def test_remove_old_events_empty():
    tracker = counttracker.CountTracker()
    current_time = time.time()

    tracker._remove_old_events(current_time)

    assert len(tracker._history) == 0


def test_remove_old_events_all_recent():
    tracker = counttracker.CountTracker()
    current_time = time.time()

    tracker._history.append(counttracker.EventSecond(current_time-2))
    tracker._history.append(counttracker.EventSecond(current_time-1))
    tracker._history.append(counttracker.EventSecond(current_time))

    assert len(tracker._history) == 3

    tracker._remove_old_events(current_time)

    assert len(tracker._history) == 3 # Nothing is removed
    assert tracker._history[0].timestamp == int(current_time - 2)
    assert tracker._history[1].timestamp == int(current_time - 1)
    assert tracker._history[2].timestamp == int(current_time)


def test_remove_old_events_all_old():
    tracker = counttracker.CountTracker()
    current_time = time.time()

    tracker._history.append(counttracker.EventSecond(current_time-303))
    tracker._history.append(counttracker.EventSecond(current_time-302))
    tracker._history.append(counttracker.EventSecond(current_time-301))

    assert len(tracker._history) == 3

    tracker._remove_old_events(current_time)

    assert len(tracker._history) == 0


def test_remove_old_events_some_recent_some_old():
    tracker = counttracker.CountTracker()
    current_time = time.time()

    tracker._history.append(counttracker.EventSecond(current_time-301))
    tracker._history.append(counttracker.EventSecond(current_time-300))
    tracker._history.append(counttracker.EventSecond(current_time-299))

    assert len(tracker._history) == 3

    tracker._remove_old_events(current_time)

    assert len(tracker._history) == 2 # One event is removed (301)
    assert tracker._history[0].timestamp == int(current_time - 300)
    assert tracker._history[1].timestamp == int(current_time - 299)


### Test log event ###
def test_log_event_one_event():
    tracker = counttracker.CountTracker()
    current_time = time.time()

    tracker.log_event()
    history = tracker._history

    assert len(history) == 0  # Event not in history yet
    assert int(tracker._last_time_logged) == int(current_time)
    assert tracker._last_time_logged_count == 1


def test_log_event_previous_event_is_same_time():
    tracker = counttracker.CountTracker()
    current_time = time.time()

    tracker.log_event()
    tracker.log_event()
    history = tracker._history

    assert len(history) == 0  # Events not in history yet
    assert tracker._last_time_logged == int(current_time)
    assert tracker._last_time_logged_count == 2


def test_log_event_previous_event_is_different_time():
    tracker = counttracker.CountTracker()
    current_time = time.time()

    # previous_second = counttracker.EventSecond(current_time - 1)
    # previous_second.count += 1
    # tracker._history.append(previous_second)
    tracker._last_time_logged = int(current_time-1)
    tracker._last_time_logged_count = 1

    tracker.log_event()
    history = tracker._history

    assert len(history) == 1  # Last event is not in history yet
    assert history[0].timestamp == int(current_time - 1)
    assert history[0].count == 1  # old event second has count 1


### Test get_event_counts ###
def test_get_event_counts_none():
    tracker = counttracker.CountTracker()

    assert tracker.get_event_counts(0) == 0  # No events
    assert tracker.get_event_counts(1) == 0  # No events
    assert tracker.get_event_counts(400) == 0  # No events


def test_get_event_counts_invalid_type():
    tracker = counttracker.CountTracker()

    with pytest.raises(AssertionError):
        tracker.get_event_counts(-1)  # Duration can't be negative
    with pytest.raises(AssertionError):
        tracker.get_event_counts(1.5)  # Duration must be integer


def test_get_event_counts_some():
    current_time = time.time()
    tracker = counttracker.CountTracker()

    es0 = counttracker.EventSecond(current_time - 20)
    es0.count = 1
    es1 = counttracker.EventSecond(current_time - 10)
    es1.count = 2
    es2 = counttracker.EventSecond(current_time - 5)
    es2.count = 5

    tracker._history.append(es0)
    tracker._history.append(es1)
    tracker._history.append(es2)

    assert tracker.get_event_counts(30) == 8  # All events
    assert tracker.get_event_counts(15) == 7
    assert tracker.get_event_counts(7) == 5
    assert tracker.get_event_counts(5) == 0  # Don't include the timestamp 5 seconds away
    assert tracker.get_event_counts(600) == 8  # Treat 600 seconds as 5 minutes


def test_get_event_counts_one_event_logged():
    current_time = time.time()
    tracker = counttracker.CountTracker()

    tracker.log_event()

    assert tracker.get_event_counts(1) == 1


### Integration testing ###
def test_log_for_longer_than_max_time():
    max_time = 2  # 2 seconds
    total_time_logged = 3  # 3 seconds

    tracker = counttracker.CountTracker()
    start = time.time()

    # Modify time limit for testing
    tracker._MEMORY_TIME_LIMIT = max_time

    # Log 3 events for 3 seconds, 1 event per second
    total_events_logged = 0
    while time.time() - start < total_time_logged:
        tracker.log_event()
        total_events_logged += 1
        time.sleep(1)

    total_events_retained = tracker.get_event_counts(total_time_logged)

    assert total_events_retained < total_events_logged  # Some events should be 'forgotten' from history


### Test load ###
# Must be able to handle 1 million events per second
def test_million_events():
    tracker = counttracker.CountTracker()

    start = time.time()

    # Log 2 million events
    for _ in range(2000000):
        tracker.log_event()

    end = time.time()

    total_time = end - start

    assert tracker.get_event_counts(4) == 2000000
    assert total_time <= 2