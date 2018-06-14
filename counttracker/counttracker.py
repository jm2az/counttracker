from collections import deque
import time

from .event_second import EventSecond

class CountTracker:
    """
    Keeps track of the counts of events that have happened over the past 5 minutes.
    Precision is to the current second. So for example, if an event happens at 5:50 and 12.34 seconds,
    it will be considered to have happened at 5:50 and 12 seconds, truncating the milliseconds associated.
    """
    def __init__(self):
        # History is a double ended queue to allow for fast pops on the left and fast appends on the right.
        # It will remain sorted by timestamp, with earlier times occurring further to the left,
        #   and later times occurring further to the right
        # Events that occur earlier than the MEMORY_TIME_LIMIT will be removed in history
        self._MEMORY_TIME_LIMIT = 300  # 5 minutes * 60 seconds per minute

        self._history = deque(maxlen=self._MEMORY_TIME_LIMIT)  # Prevents the queue from getting too long
        self._last_time_cleared = time.time()
        self._last_time_logged = None
        self._last_time_logged_count = 0


    def _remove_old_events(self, current_time):
        """
        Remove old events from history
        An old event is one that occurred more than MEMORY_TIME_LIMIT seconds before the current time
        :param current_time: time in seconds
        :return: None
        """
        oldest_event_second_allowed = EventSecond(current_time - self._MEMORY_TIME_LIMIT)

        while True:
            try:
                oldest_event_second = self._history[0]
            except IndexError:
                # history is empty
                break
            if oldest_event_second < oldest_event_second_allowed:
                # The oldest event second is outside the accepted amount of time to keep track of
                # Remove it from history and check the next oldest
                self._history.popleft()
            else:
                # The oldest event second is still recent enough to keep track of
                break

    def _log_latest_second(self):
        """
        Store the latest second into history if there is anything 'cached'

        :return: None
        """
        if self._last_time_logged is not None:
            ts = EventSecond(float(self._last_time_logged))
            ts.count = self._last_time_logged_count
            self._history.append(ts)

    def log_event(self):
        """
        Log event at the current time (second).

        If an event has already occurred at the current second, increase that second's count by 1.
        Otherwise, append a 'cached' second.

        :return: None
        """

        # Log current event
        current_time = time.time()

        # Check if the current second is the same as last.
        # If so, then increase that second's counter by 1.
        if self._last_time_logged == int(current_time):
            # Increase counter of last timestamp by 1
            self._last_time_logged_count += 1
        else:
            # Must add new Event Second to history because this is a new second
            self._log_latest_second()
            self._last_time_logged = int(current_time)
            self._last_time_logged_count = 1

    def get_event_counts(self, duration):
        """
        Get the number of events that have happened in the past X seconds, specified by 'duration'.
        This includes events that have been logged at the current second, but does not include
        events loggest at (current_time - duration).
          As an example, if we are calling get_event_counts(4) at time 20, it will return
          the events that happened at time 17, 18, 19, and 20.

        :param duration: integer: Number of seconds into the past to count events of
        :return: Total number of events that occurred in the past 'duration' seconds
        """
        current_time = time.time()

        assert duration >= 0, "Duration must be a nonnegative integer"
        assert isinstance(duration, int), "Duration must be a nonnegative integer"

        self._log_latest_second()

        # Remove old events
        self._remove_old_events(current_time)

        # duration should not be longer than the memory time limit
        if duration > self._MEMORY_TIME_LIMIT:
            duration = self._MEMORY_TIME_LIMIT

        total_count = 0
        earliest_time_to_count = EventSecond(current_time - duration)
        index = len(self._history) - 1

        # Continue going backward starting from the end of history
        #   until we either exhaust all the history or find a timestamp that's too early
        while index >= 0 and self._history[index] > earliest_time_to_count:
            total_count += self._history[index].count
            index -= 1

        return total_count
