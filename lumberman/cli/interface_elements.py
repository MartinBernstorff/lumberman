from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, Union

from rich import print

if TYPE_CHECKING:
    from types import TracebackType

    from ..stack.manipulator import QueueManipulator
    from ..stack.navigator import QueueNavigator


@dataclass
class QueueOperation:
    stack_manipulator: "QueueManipulator"
    stack_navigator: "QueueNavigator"
    sync_time: Literal["enter", "exit", "none"] = "enter"
    sync_pull_requests: bool = True

    def __call__(
        self, sync_pull_requests: bool, sync_time: Literal["enter", "exit", "none"] = "enter"
    ) -> "QueueOperation":
        self.sync_pull_requests = sync_pull_requests
        self.sync_time = sync_time
        return self

    def __enter__(self):
        print(":arrows_clockwise: [bold green]Syncing with remote...[/bold green]")
        if self.sync_time == "enter":
            self.stack_manipulator.sync(sync_pull_requests=self.sync_pull_requests)

    def __exit__(
        self, exc_type: Union[type, None], exc_val: Exception, exc_tb: "TracebackType"
    ) -> None:
        if self.sync_time == "exit" and exc_type is not None:
            self.stack_manipulator.sync(sync_pull_requests=self.sync_pull_requests)
        self.stack_navigator.log()
