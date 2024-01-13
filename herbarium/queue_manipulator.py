from typing import Protocol

from .issue_parser import IssueParser
from .issue_service import Issue
from .subprocess_utils import interactive_cmd


class QueueManipulator(Protocol):
    issue_parser: IssueParser
    issue: Issue

    def fork(self):
        ...

    def add(self):
        ...


class GraphiteManipulator(QueueManipulator):
    issue_parser: IssueParser
    issue: Issue

    def __post_init__(self):
        self.issue_info = self.issue_parser.get_issue_info(issue=self.issue)

    def fork(self):
        interactive_cmd(
            f'gt create {self.issue_info.branch_title} --all -m "{self.issue_info.first_commit_str}"'
        )

    def add(self):
        interactive_cmd(
            f'gt create {self.issue_info.branch_title} --all --insert -m "{self.issue_info.first_commit_str}"'
        )
        interactive_cmd(f'git commit --allow-empty -m "{self.issue_info.first_commit_str}"')
