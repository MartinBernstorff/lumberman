import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Protocol

from ..cli.subprocess_utils import shell_output
from .title_parser import IssueTitle, parse_issue_title

if TYPE_CHECKING:
    from collections.abc import Sequence


@dataclass(frozen=True)
class Issue:
    entity_id: Optional[str]
    title: IssueTitle
    description: str


class IssueProvider(Protocol):
    def setup(self) -> None:
        """Any setup needed, including installing CLI tools, etc."""
        ...

    def get_latest_issues(self, in_progress_label: str) -> "Sequence[Issue]":
        ...

    def get_issues_assigned_to_me(self, in_progress_label: str) -> "Sequence[Issue]":
        ...

    def get_current_issue(self) -> Optional[Issue]:
        ...

    def label_issue(self, issue: Issue, label: str) -> None:
        ...

    def assign(self, issue: Issue, assignee: str) -> None:
        ...


class GithubIssueProvider(IssueProvider):
    def setup(self) -> None:
        pass

    def _values_to_issue(self, values: dict[str, str]) -> Issue:
        parsed_title = parse_issue_title(values["title"])
        return Issue(
            entity_id=str(values["number"]), title=parsed_title, description=values["body"]
        )

    def get_latest_issues(self, in_progress_label: str) -> "Sequence[Issue]":
        latest_issues = shell_output(
            f"gh issue list --limit 10 --json number,title,body --search 'is:open -label:{in_progress_label}'"
        )

        if latest_issues is None:
            return []

        return self._parse_github_json_str(latest_issues)

    def get_issues_assigned_to_me(self, in_progress_label: str) -> "Sequence[Issue]":
        """Get issues assigned to current user on current repo"""
        my_issues_cmd = shell_output(
            f"gh issue list --assignee @me  --search '-label:{in_progress_label}' --json number,title,body"
        )

        if my_issues_cmd is None:
            return []

        return self._parse_github_json_str(my_issues_cmd)

    def _parse_github_json_str(self, issue_str: str) -> "Sequence[Issue]":
        values = json.loads(issue_str)
        parsed_output = [self._values_to_issue(v) for v in values]
        return parsed_output

    def _create_label(self, label: str) -> None:
        shell_output(f"gh label create {label}")

    def _add_label_to_issue(self, issue: Issue, label: str) -> None:
        shell_output(f'gh issue edit "{issue.entity_id}" --add-label "{label}"')

    def get_current_issue(self) -> Optional[Issue]:
        current_branch: str = shell_output("git rev-parse --abbrev-ref HEAD")  # type: ignore

        branch_items = current_branch.split("/")

        if len(branch_items) != 3:
            return None

        return Issue(
            entity_id=branch_items[1],
            title=IssueTitle(prefix=branch_items[0], content=branch_items[2]),
            description="",
        )

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

    def assign(self, issue: Issue, assignee: str) -> None:
        if issue.entity_id:
            shell_output(f"gh issue edit {int(issue.entity_id)} --add-assignee {assignee}")
