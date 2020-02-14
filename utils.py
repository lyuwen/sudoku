import signal
import numpy as np
from contextlib import contextmanager


@contextmanager
def timeout(time):
    # Register a function to raise a TimeoutError on the signal.
    signal.signal(signal.SIGALRM, raise_timeout)
    # Schedule the signal to be sent after ``time``.
    signal.alarm(time)

    try:
        yield
    except TimeoutError:
        pass
    finally:
        # Unregister the signal so it won't be triggered
        # if the timeout is not reached.
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


class TimeoutError(RuntimeError):
    pass


def raise_timeout(signum, frame):
    raise TimeoutError


def count_nonzero_unique(arr):
    unique, counts = np.unique(arr, return_counts=True)
    return counts[unique.nonzero()]
