from lumberman.cli.config import STACK_NAVIGATOR
from lumberman.cli.location import FullLocation, LocationCLIOption

from ..git import StagingMigrater
from .config import STACK_OP


def trunk():
    """Go to the trunk of the stack."""
    with STACK_OP(sync_time="none", sync_pull_requests=False):
        STACK_NAVIGATOR.trunk()


def bottom():
    """Go to the bottom of the stack."""
    with STACK_OP(sync_time="none", sync_pull_requests=False):
        STACK_NAVIGATOR.bottom()


def down():
    """Go to the item below the current one."""
    with STACK_OP(sync_time="none", sync_pull_requests=False):
        STACK_NAVIGATOR.down()


def up():
    """Go to the item above the current one."""
    with STACK_OP(sync_time="none", sync_pull_requests=False):
        STACK_NAVIGATOR.up()


def top():
    """Go to the top of the stack."""
    with STACK_OP(sync_time="none", sync_pull_requests=False):
        STACK_NAVIGATOR.top()


def log():
    """Print the current stack status."""
    STACK_NAVIGATOR.log()


def checkout():
    """Prompt to checkout an item in the stack."""
    with StagingMigrater():
        STACK_NAVIGATOR.checkout()


def navigate_to_insert_location(location: LocationCLIOption):
    match location.to_full_location:
        case FullLocation.trunk:
            STACK_NAVIGATOR.trunk()
        case FullLocation.bottom:
            STACK_NAVIGATOR.bottom()
        case FullLocation.top:
            STACK_NAVIGATOR.top()
        case FullLocation.up:
            pass
        case FullLocation.down:
            STACK_NAVIGATOR.down()
