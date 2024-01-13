import json
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Optional, Protocol

from .issue_title_parser import parse_issue_title
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

    def get_latest_issues(self, in_progress_label: str) -> Sequence[Issue]:
        ...

    def get_issues_assigned_to_me(self, in_progress_label: str) -> Sequence[Issue]:
        ...

    def label_issue(self, issue: Issue, label: str) -> None:
        ...


# XXX: Add get_recent_issues(n: int) to issue_service


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

    def get_latest_issues(self, in_progress_label: str) -> Sequence[Issue]:
        latest_issues = shell_output(
            f"gh issue list --limit 10 --json number,title --search 'is:open -label:{in_progress_label}'"
        )

        if latest_issues is None:
            return []

        return self._parse_github_json_str(latest_issues)

    def get_issues_assigned_to_me(self, in_progress_label: str) -> Sequence[Issue]:
        """Get issues assigned to current user on current repo"""
        my_issues_cmd = shell_output(
            f"gh issue list --search 'is:open assignee:@me -label:{in_progress_label}' --json number,title"
        )

        if my_issues_cmd is None:
            return []

        return self._parse_github_json_str(my_issues_cmd)

    def _parse_github_json_str(self, issue_str: str) -> Sequence[Issue]:
        values = json.loads(issue_str)
        parsed_output = [self._values_to_issue(v) for v in values]
        return parsed_output

    def _create_label(self, label: str) -> None:
        shell_output(f"gh label create {label}")

    def _add_label_to_issue(self, issue: Issue, label: str) -> None:
        shell_output(f'gh issue edit "{issue.entity_id}" --add-label "{label}"')

    def label_issue(self, issue: Issue, label: str) -> None:
        if not issue.entity_id:
            return
        try:
            self._add_label_to_issue(issue, label)
        except Exception:
            try:
                self._create_label(label)
                self._add_label_to_issue(issue, label)
            except Exception as e:
                raise RuntimeError(f"Error labeling issue {issue.entity_id} with {label}") from e
