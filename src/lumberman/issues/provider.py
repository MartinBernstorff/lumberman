from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from lumberman.issues.title_parser import IssueTitle

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence


@dataclass
class IssueComment:
    id: str
    author_login: str
    body: str
    url: str


def _parse_issue_comment(comment_json: "Mapping[str, str]") -> IssueComment:
    return IssueComment(
        id=comment_json["id"],  # type: ignore
        body=comment_json["body"],  # type: ignore
        url=comment_json["url"],  # type: ignore
        author_login=comment_json["author"]["login"],  # type: ignore
    )


@runtime_checkable
class Issue(Protocol):
    title: IssueTitle

    def render(self) -> str: ...


@dataclass
class LocalIssue(Issue):
    """Issue created by entering a title in the CLI"""

    title: IssueTitle

    def render(self) -> str:
        return self.title.content


@runtime_checkable
class RemoteIssue(Protocol):
    """Issue created by a remote source (e.g. Github)"""

    entity_id: str
    description: str

    def label(self, label: str) -> None: ...

    def assign(self, assignee: str) -> None: ...

    def get_comments(self) -> "Sequence[IssueComment]": ...


class IssueProvider(Protocol):
    def setup(self) -> None:
        """Any setup needed, including installing CLI tools, etc."""
        ...

    def get_latest_issues(self, in_progress_label: str) -> "Sequence[Issue]": ...

    def get_issues_assigned_to_me(self, in_progress_label: str) -> "Sequence[Issue]": ...

    def get_current_issue(self) -> "Issue | None": ...
