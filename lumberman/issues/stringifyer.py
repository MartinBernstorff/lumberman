from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .provider import GithubIssue


@dataclass(frozen=True)
class IssueInfo:
    branch_title: str
    first_commit_str: str


class IssueStringifyer(Protocol):
    def get_issue_info(self, issue: "GithubIssue") -> IssueInfo:
        ...


def sanitise_text_for_bash(input_string: str) -> str:
    char_to_remove = ["`"]
    for character in char_to_remove:
        input_string = input_string.replace(character, "")
    return input_string


class DefaultIssueStringifyer(IssueStringifyer):
    def get_issue_info(self, issue: "GithubIssue") -> IssueInfo:
        return IssueInfo(
            branch_title=self._get_branch_title(issue=issue),
            first_commit_str=self._get_first_commit_str(issue=issue),
        )

    def _get_branch_title(self, issue: "GithubIssue") -> str:
        branch_title = ""
        branch_title += f"{issue.title.prefix}/" if issue.title.prefix else ""
        branch_title += f"{issue.entity_id}/" if issue.entity_id else ""
        branch_title += issue.title.content
        return sanitise_text_for_bash(branch_title)

    def _get_first_commit_str(self, issue: "GithubIssue") -> str:
        first_commit_str = ""
        first_commit_str += issue.title.prefix if issue.title.prefix else ""
        first_commit_str += f"(#{issue.entity_id})" if issue.entity_id else ""
        first_commit_str += ": " if first_commit_str else first_commit_str
        first_commit_str += issue.title.content
        first_commit_str += (
            f"""

Fixes #{issue.entity_id}"""
            if issue.entity_id
            else ""
        )

        return sanitise_text_for_bash(first_commit_str)
