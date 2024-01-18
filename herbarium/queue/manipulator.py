from dataclasses import dataclass
from typing import Protocol

from ..cli.subprocess_utils import interactive_cmd
from ..issues.model import Issue
from ..issues.stringifyer import IssueStringifyer


class QueueManipulator(Protocol):
    issue_parser: IssueStringifyer

    def fork(self, issue: Issue):
        ...

    def add(self, issue: Issue):
        ...

    def delete(self):
        ...

    def move(self):
        ...

    def sync(self, automerge: bool = False, squash: bool = False, draft: bool = True):
        ...


@dataclass(frozen=True)
class GraphiteManipulator(QueueManipulator):
    issue_parser: IssueStringifyer

    def _new_branch(self, insert: bool, issue: Issue):
        issue_info = self.issue_parser.get_issue_info(issue)

        create_command = f'gt create "{issue_info.branch_title}" -m "{issue_info.first_commit_str}" --no-interactive'
        create_command += " --insert" if insert else ""

        print(f"Creating branch with command: {create_command}")
        interactive_cmd(create_command)
        interactive_cmd("git add -A")
        interactive_cmd(f'git commit --allow-empty -m "{issue_info.first_commit_str}"')

    def fork(self, issue: Issue):
        self._new_branch(insert=False, issue=issue)

    def add(self, issue: Issue):
        self._new_branch(insert=True, issue=issue)

    def delete(self):
        interactive_cmd("gt delete")

    def move(self):
        interactive_cmd("gt move")

    def sync(self, automerge: bool = False, squash: bool = False, draft: bool = True):
        interactive_cmd("gt sync --force --restack --delete")

        if squash:
            interactive_cmd("gt squash --no-edit")

        command = "gt submit --no-edit --stack"
        if draft:
            command += " --draft"
        else:
            command += " --publish"

        if automerge:
            command += " --merge-when-ready"
        interactive_cmd(command)
