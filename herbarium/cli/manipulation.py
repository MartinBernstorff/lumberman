from rich import print

from .config import ISSUE_CONTROLLER, QUEUE_MANIPULATOR, QUEUE_NAVIGATOR, QUEUE_OP
from .location import Location, LocationCLIOption


def add(location: LocationCLIOption = Location.after):
    """Add a new item to the current queue. Defaults to adding an item in between the current item and the next item."""
    with QUEUE_OP(sync_time="exit", sync_remote=False):
        selected_issue = ISSUE_CONTROLLER.select_issue()

        if location == Location.front:
            QUEUE_NAVIGATOR.go_to_front()
        elif location == Location.back:
            QUEUE_NAVIGATOR.go_to_back()
        elif location == Location.after:
            pass
        elif location == Location.before:
            QUEUE_NAVIGATOR.before()

        QUEUE_MANIPULATOR.add(selected_issue)
        ISSUE_CONTROLLER.label_issue_in_progress(selected_issue)


def move():
    """Move the current item to a new location in the queue."""
    with QUEUE_OP(sync_time="exit", sync_remote=False):
        QUEUE_MANIPULATOR.move()


def delete():
    """Delete a selected item from the queue."""
    with QUEUE_OP(sync_time="exit", sync_remote=False):
        QUEUE_MANIPULATOR.delete()


def fork(location: LocationCLIOption = Location.front):
    """Fork into a new queue and add an item. Defaults to forking from the first item in the current queue."""
    with QUEUE_OP(sync_time="enter", sync_remote=False):
        selected_issue = ISSUE_CONTROLLER.select_issue()

        if location == Location.front:
            QUEUE_NAVIGATOR.go_to_second_in_line()
        elif location == Location.back:
            QUEUE_NAVIGATOR.go_to_next_to_last()
        elif location == Location.after:
            pass  # No need to do anything, already in the correct location
        elif location == Location.before:
            QUEUE_NAVIGATOR.before()

        QUEUE_MANIPULATOR.fork(selected_issue)
        ISSUE_CONTROLLER.label_issue_in_progress(selected_issue)


def new():
    """Start a new queue on top of trunk."""
    with QUEUE_OP(sync_time="exit", sync_remote=False):
        selected_issue = ISSUE_CONTROLLER.select_issue()
        QUEUE_NAVIGATOR.go_to_front()
        QUEUE_MANIPULATOR.fork(selected_issue)
        ISSUE_CONTROLLER.label_issue_in_progress(selected_issue)


def sync(automerge: bool = False, draft: bool = False, squash: bool = False):
    """Synchronize all state, ensuring the queue is internally in sync, and in sync with the remote. Creates PRs if needed."""
    with QUEUE_OP(sync_time="none", sync_remote=False):
        QUEUE_MANIPULATOR.sync(automerge=automerge, squash=squash, draft=draft, sync_remote=True)
        print(":rocket: [bold green]Stack synced![/bold green]")
