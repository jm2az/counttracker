from collections import deque
import time

from .event_second import EventSecond

class CountTracker:
    """
    Keeps track of the counts of events that have happened over the past 5 minutes.
    Precision is to the current second.
    """
    def __init__(self):
        # History is a double ended queue to allow for fast pops on the left and fast appends on the right.
        # It will remain sorted by timestamp, with earlier times occurring further to the left,
        #   and later times occurring further to the right
        # Events that occur earlier than the MEMORY_TIME_LIMIT will be removed in history
        self._history = deque()

        self._MEMORY_TIME_LIMIT = 300  # 5 minutes * 60 seconds per minute

    def _current_time_is_in_history(self, current_time):
        """

        :param current_time: time in seconds
        :return: True if the current time has already been logged, else False
        """
        try:
            last_event = self._history[-1]

            if last_event.timestamp == int(current_time):
                return True
            else:
                return False
        except IndexError:
            # History is empty
            return False

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


    def log_event(self):
        """
        Log event at the current time (second).

        If an event has already occurred at the current second, increase that second's count by 1.
        Otherwise, append a new second with a count of 1.

        Also deletes records of events that occurred before MEMORY_TIME_LIMIT before the current time

        :return: None
        """

        # Log current event
        current_time = time.time()

        if self._current_time_is_in_history(current_time):
            # Increase counter of last timestamp by 1
            self._history[-1].log_event()
        else:
            # Must add new Event Second to history because this is a new second
            new_second = EventSecond(current_time)
            new_second.log_event()
            self._history.append(new_second)

        # Remove old events
        self._remove_old_events(current_time)

    def get_event_counts(self, duration):
        """
        Get the number of events that have happened in the past X minutes, specified by 'duration'

        :param duration: Number of seconds into the past to count events of
        :return: total number of events that occurred in the past 'duration' seconds
        """
        current_time = time.time()

        assert duration >= 0, "Duration must be a nonnegative integer"
        assert isinstance(duration, int), "Duration must be a nonnegative integer"

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
