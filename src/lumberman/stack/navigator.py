from dataclasses import dataclass
from typing import Protocol

from rich import box, print  # noqa: A004
from rich.panel import Panel

from ..cli.subprocess_utils import interactive_cmd, shell_output
from ..git import StagingMigrater


class QueueNavigator(Protocol):
    def trunk(self): ...

    def bottom(self): ...

    def top(self): ...

    def down(self): ...

    def up(self): ...

    def log(self): ...

    def checkout(self): ...


@dataclass(frozen=True)
class GraphiteNavigator(QueueNavigator):
    def trunk(self):
        with StagingMigrater():
            trunk_branch = shell_output("gt trunk")
            if trunk_branch is None:
                raise RuntimeError("Failed to get trunk branch")
            interactive_cmd(f"git checkout {trunk_branch}")

    def bottom(self):
        with StagingMigrater():
            interactive_cmd("gt bottom")

    def top(self):
        with StagingMigrater():
            interactive_cmd("gt top")

    def down(self):
        interactive_cmd("gt down")

    def up(self):
        interactive_cmd("gt up")

    def log(self):
        result: str = shell_output("gt log short")  # type: ignore
        print(
            "\n",
            Panel(result, title="Top", subtitle="Bottom", expand=False, box=box.HORIZONTALS),
            "\n",
        )

    def checkout(self):
        interactive_cmd("gt checkout")
