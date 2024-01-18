from rich import print

from .config import ISSUE_CONTROLLER, STACK_MANIPULATOR, STACK_NAVIGATOR, STACK_OP
from .location import Location, LocationCLIOption


def add(location: LocationCLIOption = Location.up):
    """Add a new item to the current stack. Defaults to adding an item in between the current item and the next item."""
    with STACK_OP(sync_time="exit", sync_remote=False):
        selected_issue = ISSUE_CONTROLLER.select_issue()

        if location == Location.bottom:
            STACK_NAVIGATOR.bottom()
        elif location == Location.top:
            STACK_NAVIGATOR.top()
        elif location == Location.up:
            pass
        elif location == Location.down:
            STACK_NAVIGATOR.down()

        STACK_MANIPULATOR.add(selected_issue)
        ISSUE_CONTROLLER.label_issue_in_progress(selected_issue)


def move():
    """Move the current item to a new location in the stack."""
    with STACK_OP(sync_time="exit", sync_remote=False):
        STACK_MANIPULATOR.move()


def delete():
    """Delete a selected item from the stack."""
    with STACK_OP(sync_time="exit", sync_remote=False):
        STACK_MANIPULATOR.delete()


def fork(location: LocationCLIOption = Location.bottom):
    """Fork into a new stack and add an item. Defaults to forking from the first item in the current stack."""
    with STACK_OP(sync_time="enter", sync_remote=False):
        selected_issue = ISSUE_CONTROLLER.select_issue()

        if location == Location.bottom:
            STACK_NAVIGATOR.bottom()
            STACK_NAVIGATOR.up()
        elif location == Location.top:
            STACK_NAVIGATOR.top()
            STACK_NAVIGATOR.down()
        elif location == Location.up:
            pass  # No need to do anything, already in the correct location
        elif location == Location.down:
            STACK_NAVIGATOR.down()

        STACK_MANIPULATOR.fork(selected_issue)
        ISSUE_CONTROLLER.label_issue_in_progress(selected_issue)


def new():
    """Start a new stack on top of trunk."""
    with STACK_OP(sync_time="exit", sync_remote=False):
        selected_issue = ISSUE_CONTROLLER.select_issue()
        STACK_NAVIGATOR.bottom()
        STACK_MANIPULATOR.fork(selected_issue)
        ISSUE_CONTROLLER.label_issue_in_progress(selected_issue)


def sync(automerge: bool = False, draft: bool = False, squash: bool = False):
    """Synchronize all state, ensuring the stack is internally in sync, and in sync with the remote. Creates PRs if needed."""
    with STACK_OP(sync_time="none", sync_remote=False):
        STACK_MANIPULATOR.sync(automerge=automerge, squash=squash, draft=draft, sync_remote=True)
        print(":rocket: [bold green]Stack synced![/bold green]")
