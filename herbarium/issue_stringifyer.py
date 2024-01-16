from dataclasses import dataclass
from typing import Protocol

from .issue_service import Issue


@dataclass(frozen=True)
class IssueInfo:
    branch_title: str
    first_commit_str: str


class IssueStringifyer(Protocol):
    def get_issue_info(self, issue: Issue) -> IssueInfo:
        ...


def sanitise_text_for_bash(input_string: str) -> str:
    char_to_remove = ["`"]
    for character in char_to_remove:
        input_string = input_string.replace(character, "")
    return input_string


class DefaultIssueStringifyer(IssueStringifyer):
    def get_issue_info(self, issue: Issue) -> IssueInfo:
        return IssueInfo(
            branch_title=self._get_branch_title(issue=issue),
            first_commit_str=self._get_first_commit_str(issue=issue),
        )

    def _get_branch_title(self, issue: Issue) -> str:
        prefix_section = f"{issue.prefix}/" if issue.prefix is not None else ""
        entity_id_section = f"{issue.entity_id}/" if issue.entity_id is not None else ""
        return sanitise_text_for_bash(f"{prefix_section}{entity_id_section}{issue.description}")

    def _get_first_commit_str(self, issue: Issue) -> str:
        first_commit_str = ""
        first_commit_str += issue.prefix if issue.prefix is not None else ""
        first_commit_str += f"(#{issue.entity_id})" if issue.entity_id is not None else ""
        first_commit_str += ": " if first_commit_str else first_commit_str
        first_commit_str += issue.description
        first_commit_str += (
            f"""

Fixes #{issue.entity_id}"""
            if issue.entity_id is not None
            else ""
        )

        return sanitise_text_for_bash(first_commit_str)
