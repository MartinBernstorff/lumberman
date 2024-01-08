from dataclasses import dataclass
from types import TracebackType

import typer

from herbarium.subprocess_utils import shell_output


def has_uncommitted_changes() -> bool:
    """Returns True if there are uncommitted changes in the git repo"""
    try:
        shell_output("git diff --quiet")  # Any changes in the working tree
        shell_output("git diff --cached --quiet")  # Any changes in the index
        return False
    except RuntimeError:
        return True


def commit_unstaged() -> None:
    """Commits any unstaged changes"""
    if not has_uncommitted_changes():
        return

    commit_msg = typer.prompt(
        "You have uncommitted changes. Please enter a commit message, or leave blank to abort.",
        default="Misc.",
    )
    if commit_msg == "":
        raise RuntimeError("Aborting because of uncommitted changes")

    shell_output(f'git commit -m "{commit_msg}"')


@dataclass
class StagingMigrater:
    has_stashed: bool = False

    def __enter__(self):
        if not has_uncommitted_changes():
            return

        shell_output("git stash")
        self.has_stashed = True

    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: TracebackType) -> None:
        """Applies the latest stash"""
        if not self.has_stashed:
            return

        shell_output("git stash apply")
