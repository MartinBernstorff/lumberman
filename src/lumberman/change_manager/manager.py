from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

from lumberman.cli.subprocess_utils import interactive_cmd

if TYPE_CHECKING:
    from lumberman.issues.provider import Issue
    from lumberman.issues.stringifyer import IssueStringifyer


class ChangeManager(Protocol):
    def fork(self, issue: "Issue"):
        """Create a new item, forking from the current item."""
        ...

    def sync(self, automerge: bool = False, squash: bool = False, draft: bool = True):
        ...


from typing import Protocol


class Forge(Protocol):
    def sync(self, automerge: bool = False, squash: bool = False, draft: bool = True):
        ...


class GithubForge(Forge):
    def sync(self, automerge: bool = False, squash: bool = False, draft: bool = True):
        cmd = "gh pr create"
        if draft:
            cmd += " --draft"
        if automerge:
            cmd += " --auto"
        if squash:
            cmd += " --squash"
        interactive_cmd(cmd)


from typing import Protocol


class LocalManager(Protocol):
    def fork(self, issue: "Issue"):
        ...


@dataclass(frozen=True)
class GitLocalManager(LocalManager):
    stringifyer: "IssueStringifyer"

    def fork(self, issue: "Issue"):
        interactive_cmd(f"git checkout -b {issue.title.content}")
        interactive_cmd("git add -A")
        interactive_cmd(f'git commit --allow-empty -m "{issue.title.content}"')


@dataclass(frozen=True)
class LocalAndForge(ChangeManager):
    forge: Forge
    local_manager: LocalManager

    def fork(self, issue: "Issue"):
        self.local_manager.fork(issue)
        self.forge.sync()

    def sync(self, automerge: bool = False, squash: bool = False, draft: bool = True):
        self.forge.sync(automerge=automerge, squash=squash, draft=draft)
