from collections.abc import Sequence
from typing import Protocol

import questionary
from rich.console import Console

from .issue_service import Issue

console = Console()


class IssuePresenter(Protocol):
    def select_issue_dialog(self, issues: Sequence[Issue]) -> Issue:
        ...


class DefaultIssuePresenter(IssuePresenter):
    def select_issue_dialog(self, issues: Sequence[Issue]) -> Issue:
        selected_issue_title = questionary.select(
            "I found these issues for you. Which one do you want to work on?",
            choices=[issue.title for issue in issues],
            qmark="",
        ).ask()

        return next(issue for issue in issues if issue.title == selected_issue_title)
