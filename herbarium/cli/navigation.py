from .config import QUEUE_NAVIGATOR, QUEUE_OP


def front():
    """Go to the front of the queue."""
    with QUEUE_OP(sync_time="none", sync_remote=False):
        QUEUE_NAVIGATOR.go_to_front()


def before():
    """Go to the item before the current one."""
    with QUEUE_OP(sync_time="none", sync_remote=False):
        QUEUE_NAVIGATOR.before()


def after():
    """Go to the item after the current one."""
    with QUEUE_OP(sync_time="none", sync_remote=False):
        QUEUE_NAVIGATOR.after()


def back():
    """Go to the back of the queue."""
    with QUEUE_OP(sync_time="none", sync_remote=False):
        QUEUE_NAVIGATOR.go_to_back()


def status():
    """Print the current queue status."""
    with QUEUE_OP(sync_time="none", sync_remote=False):
        QUEUE_NAVIGATOR.status()
