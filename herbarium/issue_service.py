import json
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from rich.progress import Progress, SpinnerColumn, TextColumn

from .subprocess_utils import shell


@dataclass(frozen=True)
class Issue:
    entity_id: str
    title: str


class IssueService(Protocol):
    def setup(self) -> None:
        """Any setup needed, including installing CLI tools, etc."""
        ...

    def get_issues_assigned_to_me(self) -> Sequence[Issue]:
        ...


class GithubIssueService(IssueService):
    def setup(self) -> None:
        pass

    def get_issues_assigned_to_me(self) -> Sequence[Issue]:
        """Get issues assigned to current user on current repo"""
        my_issues_cmd = shell("gh issue list --assignee='@me' --json number,title")

        if my_issues_cmd is None:
            print("No issues assigned to you, exiting")
            return []

        values = json.loads(my_issues_cmd)
        parsed_output = [Issue(entity_id=str(v["number"]), title=v["title"]) for v in values]

        return parsed_output
