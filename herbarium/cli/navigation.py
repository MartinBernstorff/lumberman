from .config import QUEUE_NAVIGATOR


def front():
    """Go to the front of the queue."""
    QUEUE_NAVIGATOR.go_to_front()


def before():
    """Go to the item before the current one."""
    QUEUE_NAVIGATOR.before()


def after():
    """Go to the item after the current one."""
    QUEUE_NAVIGATOR.after()


def back():
    """Go to the back of the queue."""
    QUEUE_NAVIGATOR.go_to_back()


def status():
    """Print the current queue status."""
    QUEUE_NAVIGATOR.status()
