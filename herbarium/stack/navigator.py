from dataclasses import dataclass
from typing import Protocol

from rich import box, print
from rich.panel import Panel

from ..cli.subprocess_utils import interactive_cmd, shell_output
from ..git import StagingMigrater


class QueueNavigator(Protocol):
    def bottom(self):
        ...

    def top(self):
        ...

    def down(self):
        ...

    def up(self):
        ...

    def status(self):
        ...


@dataclass(frozen=True)
class GraphiteNavigator(QueueNavigator):
    def bottom(self):
        with StagingMigrater():
            interactive_cmd("gt trunk")

    def top(self):
        with StagingMigrater():
            interactive_cmd("gt top")

    def down(self):
        interactive_cmd("gt down")

    def up(self):
        interactive_cmd("gt up")

    def status(self):
        result: str = shell_output("gt log short")  # type: ignore
        print(
            "\n",
            Panel(result, title="Top", subtitle="Bottom", expand=False, box=box.HORIZONTALS),
            "\n",
        )
