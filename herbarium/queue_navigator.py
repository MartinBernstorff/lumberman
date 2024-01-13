from dataclasses import dataclass
from typing import Protocol

from .git_stager import StagingMigrater
from .subprocess_utils import interactive_cmd


class QueueNavigator(Protocol):
    def go_to_front(self):
        ...

    def go_to_back(self):
        ...

    def move_up_one(self):
        ...

    def move_down_one(self):
        ...

    def status(self):
        ...


@dataclass(frozen=True)
class GraphiteNavigator(QueueNavigator):
    def go_to_front(self):
        with StagingMigrater():
            interactive_cmd("gt trunk")
        interactive_cmd("gt up")

    def go_to_back(self):
        with StagingMigrater():
            interactive_cmd("gt top")

    def move_up_one(self):
        interactive_cmd("gt up")

    def move_down_one(self):
        interactive_cmd("gt down")

    def status(self):
        interactive_cmd("gt log short --reverse")
