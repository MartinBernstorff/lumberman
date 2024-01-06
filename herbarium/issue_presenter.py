from collections.abc import Sequence
from typing import Protocol

from .issue_service import Issue
from .string_parsing import (
    get_letter_alphabet_position,
    get_letter_from_alphabet_position,
)


class IssuePresenter(Protocol):
    def select_issue_dialog(self, issues: Sequence[Issue]) -> Issue:
        ...


class DefaultIssuePresenter(IssuePresenter):
    def select_issue_dialog(self, issues: Sequence[Issue]) -> Issue:
        issue_strings = [
            f"[{get_letter_from_alphabet_position(i+1)}] #{issue.entity_id} {issue.title}"
            for i, issue in enumerate(issues)
        ]

        n_issues = len(issues)

        terminal_output = "\n".join(reversed(issue_strings))
        print(f"\n{terminal_output}\n")

        print(
            "I found these issues for you. Which do you want to work on?\n"
        )

        issue_index = (
            get_letter_alphabet_position(
                input(
                    f"[a-{get_letter_from_alphabet_position(n_issues)}]: "
                )
            )
            - 1
        )

        return issues[issue_index]
