from collections import deque
from .event_second import EventSecond

class CountTracker:
    """
    Keeps track of the counts of events that have happened over the past 5 minutes.
    Precision is to the current second.
    """
    def __init__(self):
        self._history = deque()

    def log_event(self):
        raise NotImplementedError("log_event not implemented yet.")

    def get_event_counts(self, duration):
        raise NotImplementedError("log_event not implemented yet.")
