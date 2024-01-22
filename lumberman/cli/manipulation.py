from rich import print

from .config import ISSUE_CONTROLLER, STACK_MANIPULATOR, STACK_NAVIGATOR, STACK_OP
from .location import Location, LocationCLIOption


def create(location: LocationCLIOption = Location.up):
    """Prompt to create a new item on the current stack. Defaults to creating an item in between the current item and the next item."""
    with STACK_OP(sync_time="exit", sync_remote=False):
        selected_issue = ISSUE_CONTROLLER.select_issue()

        if location == Location.trunk:
            STACK_NAVIGATOR.trunk()
        if location == Location.bottom:
            STACK_NAVIGATOR.bottom()
        if location == Location.top:
            STACK_NAVIGATOR.top()
        if location == Location.up:
            pass
        if location == Location.down:
            STACK_NAVIGATOR.down()

        STACK_MANIPULATOR.create(selected_issue)
        ISSUE_CONTROLLER.label_issue_in_progress(selected_issue)


def move():
    """Move the current item to a new location in the stack."""
    with STACK_OP(sync_time="exit", sync_remote=False):
        STACK_MANIPULATOR.move()


def delete():
    """Prompt to delete an item."""
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
        STACK_NAVIGATOR.trunk()
        STACK_MANIPULATOR.fork(selected_issue)
        ISSUE_CONTROLLER.label_issue_in_progress(selected_issue)


def sync(automerge: bool = False, draft: bool = False, squash: bool = False):
    """Synchronize all state, ensuring the stack is internally in sync, and in sync with the remote. Creates PRs if needed."""
    with STACK_OP(sync_time="none", sync_remote=False):
        STACK_MANIPULATOR.sync(automerge=automerge, squash=squash, draft=draft, sync_remote=True)
        print(":rocket: [bold green]Stack synced![/bold green]")
