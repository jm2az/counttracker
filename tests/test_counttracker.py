from .context import counttracker


def test_init():
    ct = counttracker.CountTracker()
    assert ct is not None
