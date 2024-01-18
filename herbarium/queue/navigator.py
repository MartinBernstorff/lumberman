from dataclasses import dataclass
from typing import Protocol

from rich import box, print
from rich.panel import Panel

from ..cli.subprocess_utils import interactive_cmd, shell_output
from ..git import StagingMigrater


class QueueNavigator(Protocol):
    def go_to_front(self):
        ...

    def go_to_second_in_line(self):
        ...

    def go_to_back(self):
        ...

    def go_to_next_to_last(self):
        ...

    def before(self):
        ...

    def after(self):
        ...

    def status(self):
        ...


@dataclass(frozen=True)
class GraphiteNavigator(QueueNavigator):
    def go_to_front(self):
        with StagingMigrater():
            interactive_cmd("gt trunk")

    def go_to_second_in_line(self):
        self.go_to_front()
        self.after()

    def go_to_back(self):
        with StagingMigrater():
            interactive_cmd("gt top")

    def go_to_next_to_last(self):
        self.go_to_back()
        self.before()

    def before(self):
        interactive_cmd("gt down")

    def after(self):
        interactive_cmd("gt up")

    def status(self):
        result: str = shell_output("gt log short")  # type: ignore
        print(
            "\n",
            Panel(result, title="Back", subtitle="Front", expand=False, box=box.HORIZONTALS),
            "\n",
        )
