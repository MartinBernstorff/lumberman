from dataclasses import dataclass
from types import TracebackType
from typing import Literal

from rich import print

from ..stack.manipulator import QueueManipulator
from ..stack.navigator import QueueNavigator


@dataclass
class QueueOperation:
    stack_manipulator: QueueManipulator
    stack_navigator: QueueNavigator
    sync_time: Literal["enter", "exit", "none"] = "enter"
    sync_remote: bool = True

    def __call__(
        self, sync_remote: bool, sync_time: Literal["enter", "exit", "none"] = "enter"
    ) -> "QueueOperation":
        self.sync_remote = sync_remote
        self.sync_time = sync_time
        return self

    def __enter__(self):
        print(":arrows_clockwise: [bold green]Syncing with remote...[/bold green]")
        if self.sync_time == "enter":
            self.stack_manipulator.sync(sync_remote=self.sync_remote)

    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: TracebackType) -> None:
        if self.sync_time == "exit":
            self.stack_manipulator.sync(sync_remote=self.sync_remote)
        self.stack_navigator.status()
