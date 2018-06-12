class EventSecond:
    """
    Keeps track of the number of events that have occurred at the current second in time.
    Initializes the count to zero.
    """
    __slots__ = ('timestamp', 'count')

    def __init__(self, unix_timestamp):
        """
        Initialize the instance with a count of zero

        :param unix_timestamp: float, time of the event
        """
        assert isinstance(unix_timestamp, float), "Unix timestamp must be float"
        self.timestamp = int(unix_timestamp)
        self.count = 0

    def log_event(self):
        """
        Records an additional event. Increases count by 1

        :return: None
        """
        self.count += 1

    def __eq__(self, other):
        if isinstance(other, EventSecond):
            return self.timestamp == other.timestamp
        return False

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        if isinstance(other, EventSecond):
            return self.timestamp < other.timestamp
        return False

    def __le__(self, other):
        return (self < other) or (self == other)

    def __gt__(self, other):
        return not (self <= other)

    def __ge__(self, other):
        return not (self < other)

    def __repr__(self):
        return "Time: {}, count: {}".format(self.timestamp, self.count)

