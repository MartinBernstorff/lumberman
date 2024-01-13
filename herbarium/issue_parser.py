from typing import Protocol

from .issue_service import Issue
from .parse_issue_title import sanitise_text_for_bash


class IssueParser(Protocol):
    def get_branch_title(self, issue: Issue) -> str:
        ...

    def get_first_commit_str(self, issue: Issue) -> str:
        ...


class DefaultIssueParser(IssueParser):
    def get_branch_title(self, issue: Issue) -> str:
        entity_id_section = "" if issue.entity_id is None else f"/{issue.entity_id}"
        return f"{issue.prefix}{entity_id_section}/{issue.description}"

    def get_first_commit_str(self, issue: Issue) -> str:
        if issue.entity_id is None:
            first_commit_str = f"{issue.prefix}: {issue.description}"
        else:
            first_commit_str = f"""{issue.prefix}(#{issue.entity_id}): {issue.description}

Fixes #{issue.entity_id}"""

        return sanitise_text_for_bash(first_commit_str)
