from dataclasses import dataclass
from typing import Protocol

from .issue_service import Issue
from .issue_stringifyer import IssueStringifyer
from .subprocess_utils import interactive_cmd


class QueueManipulator(Protocol):
    issue_parser: IssueStringifyer

    def fork(self, issue: Issue):
        ...

    def add(self, issue: Issue):
        ...

    def sync(self):
        ...

    def submit(self, automerge: bool = False):
        ...


@dataclass(frozen=True)
class GraphiteManipulator(QueueManipulator):
    issue_parser: IssueStringifyer

    def fork(self, issue: Issue):
        issue_info = self.issue_parser.get_issue_info(issue)
        interactive_cmd(
            f'gt create {issue_info.branch_title} --all -m "{issue_info.first_commit_str}"'
        )

    def add(self, issue: Issue):
        issue_info = self.issue_parser.get_issue_info(issue)
        interactive_cmd(
            f'gt create {issue_info.branch_title} --all --insert -m "{issue_info.first_commit_str}"'
        )
        interactive_cmd(f'git commit --allow-empty -m "{issue_info.first_commit_str}"')

    def sync(self):
        interactive_cmd("gt sync --force --restack --delete")

    def submit(self, automerge: bool = False):
        command = "gt submit -m --no-edit --publish"
        if automerge:
            command += " --merge-when-ready"
        interactive_cmd(command)
