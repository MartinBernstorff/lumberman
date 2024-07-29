from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

from lumberman.issues.provider import Issue

from ..cli.subprocess_utils import interactive_cmd

if TYPE_CHECKING:
    from ..issues.provider import Issue
    from ..issues.stringifyer import IssueStringifyer


class QueueManipulator(Protocol):
    issue_parser: "IssueStringifyer"

    def fork(self, issue: "Issue"):
        """Create a new item, forking from the current item."""
        ...

    def insert(self, issue: "Issue"):
        """Create a new item. If an item exists above the current item, insert between them."""
        ...

    def delete(self):
        ...

    def move(self):
        ...

    def sync(
        self,
        sync_pull_requests: bool = True,
        automerge: bool = False,
        squash: bool = False,
        draft: bool = True,
    ):
        ...


@dataclass(frozen=True)
class GraphiteManipulator(QueueManipulator):
    issue_parser: "IssueStringifyer"

    def _new_branch(self, insert: bool, issue: "Issue"):
        issue_info = self.issue_parser.get_issue_info(issue)

        create_command = f'gt create "{issue_info.branch_title}" -m "{issue_info.first_commit_str}" --no-interactive'
        create_command += " --insert" if insert else ""

        print(f"Creating branch with command: {create_command}")
        interactive_cmd(create_command)
        interactive_cmd("git add -A")
        interactive_cmd(f'git commit --allow-empty -m "{issue_info.first_commit_str}"')

    def fork(self, issue: "Issue"):
        self._new_branch(insert=False, issue=issue)

    def insert(self, issue: "Issue"):
        self._new_branch(insert=True, issue=issue)

    def delete(self):
        interactive_cmd("gt delete")

    def move(self):
        interactive_cmd("gt move")

    def sync(
        self,
        sync_pull_requests: bool = True,
        automerge: bool = False,
        squash: bool = False,
        draft: bool = True,
    ):
        if squash:
            interactive_cmd("gt squash --no-edit")

        interactive_cmd("gt sync --pull --force --restack")

        if sync_pull_requests:
            command = "gt submit --no-edit --stack"
            if draft:
                command += " --draft"
            else:
                command += " --publish"

            if automerge:
                command += " --merge-when-ready"
            interactive_cmd(command)
