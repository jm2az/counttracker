import time

from .context import counttracker


def test_init():
    tracker = counttracker.CountTracker()
    assert tracker is not None


### Test _current_time_is_in_history ###
def test_current_time_is_in_history_empty():
    tracker = counttracker.CountTracker()
    current_time = time.time()

    assert not tracker._current_time_is_in_history(int(current_time))


def test_current_time_is_in_history_false():
    tracker = counttracker.CountTracker()
    current_time = time.time()
    tracker.log_event()

    assert not tracker._current_time_is_in_history(int(current_time) + 1)


def test_current_time_is_in_history_true():
    tracker = counttracker.CountTracker()
    current_time = time.time()
    tracker.log_event()

    assert tracker._current_time_is_in_history(int(current_time))


### Test log event ###
def test_log_event_one_event():
    tracker = counttracker.CountTracker()

    current_time = time.time()

    tracker.log_event()
    history = tracker._history

    assert len(history) == 1
    assert history[0].timestamp == int(current_time)
    assert history[0].count == 1


def test_log_event_previous_event_is_same_time():
    tracker = counttracker.CountTracker()

    current_time = time.time()

    tracker.log_event()
    tracker.log_event()
    history = tracker._history

    assert len(history) == 1  # Still only one event second is logged
    assert history[0].timestamp == int(current_time)
    assert history[0].count == 2 # Two events occurred at only event second


def test_log_event_previous_event_is_different_time():
    tracker = counttracker.CountTracker()

    current_time = time.time()

    previous_second = counttracker.EventSecond(current_time - 1)
    previous_second.log_event()
    tracker._history.append(previous_second)
    tracker.log_event()
    history = tracker._history

    assert len(history) == 2  # Now two event seconds are logged
    assert history[0].timestamp != int(current_time)
    assert history[0].count == 1  # old event second has count 1
    assert history[1].count == 1  # new event second has count 1
