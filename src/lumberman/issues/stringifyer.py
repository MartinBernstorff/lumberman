from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

from lumberman.issues.provider import RemoteIssue

if TYPE_CHECKING:
    from .provider import Issue


@dataclass(frozen=True)
class IssueInfo:
    branch_title: str
    first_commit_str: str


class IssueStringifyer(Protocol):
    def get_issue_info(self, issue: "Issue") -> IssueInfo:
        ...


def sanitise_text_for_bash(input_string: str) -> str:
    char_to_remove = ["`"]
    for character in char_to_remove:
        input_string = input_string.replace(character, "")
    return input_string


class DefaultIssueStringifyer(IssueStringifyer):
    def get_issue_info(self, issue: "Issue") -> IssueInfo:
        return IssueInfo(
            branch_title=self._get_branch_title(issue=issue),
            first_commit_str=self._get_first_commit_str(issue=issue),
        )

    def _get_branch_title(self, issue: "Issue") -> str:
        branch_title: str = ""
        branch_title += f"{issue.title.prefix}/" if issue.title.prefix is not None else ""
        branch_title += f"{issue.entity_id}/" if isinstance(issue, RemoteIssue) else ""
        branch_title += issue.title.content

        return sanitise_text_for_bash(branch_title)

    def _get_first_commit_str(self, issue: "Issue") -> str:
        first_commit_str = issue.title.prefix if issue.title.prefix is not None else ""

        if isinstance(issue, RemoteIssue):
            first_commit_str += f"(#{issue.entity_id})"

        first_commit_str += ": " if first_commit_str else first_commit_str
        first_commit_str += issue.title.content

        if isinstance(issue, RemoteIssue):
            first_commit_str += f"""

Fixes #{issue.entity_id}"""

        return sanitise_text_for_bash(first_commit_str)
