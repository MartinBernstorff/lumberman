from dataclasses import dataclass
from typing import Protocol

from .git_utils import StagingMigrater
from .subprocess_utils import interactive_cmd


class QueueNavigator(Protocol):
    def go_to_front(self):
        ...


@dataclass(frozen=True)
class GraphiteNavigator(QueueNavigator):
    def go_to_front(self):
        with StagingMigrater():
            interactive_cmd("gt bottom")
        interactive_cmd("gt trunk")
