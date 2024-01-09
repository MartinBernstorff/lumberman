import json
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Optional, Protocol

from .parse_issue_title import parse_issue_title
from .subprocess_utils import shell_output


@dataclass(frozen=True)
class Issue:
    entity_id: Optional[str]
    prefix: str
    description: str


class IssueService(Protocol):
    def setup(self) -> None:
        """Any setup needed, including installing CLI tools, etc."""
        ...

    def get_issues_assigned_to_me(self) -> Sequence[Issue]:
        ...


class GithubIssueService(IssueService):
    def setup(self) -> None:
        pass

    def _values_to_issue(self, values: dict[str, str]) -> Issue:
        parsed_title = parse_issue_title(values["title"])
        return Issue(
            entity_id=str(values["number"]),
            description=parsed_title.description,
            prefix=parsed_title.prefix,
        )

    def get_issues_assigned_to_me(self) -> Sequence[Issue]:
        """Get issues assigned to current user on current repo"""
        my_issues_cmd = shell_output("gh issue list --assignee='@me' --json number,title")

        if my_issues_cmd is None:
            return []

        values = json.loads(my_issues_cmd)

        parsed_output = [self._values_to_issue(v) for v in values]

        return parsed_output
