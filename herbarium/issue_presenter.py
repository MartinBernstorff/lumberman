from collections.abc import Sequence
from typing import Protocol

import questionary
from rich.console import Console
from rich.table import Table

from .issue_service import Issue

console = Console()


class IssuePresenter(Protocol):
    def select_issue_dialog(self, issues: Sequence[Issue]) -> Issue:
        ...


class DefaultIssuePresenter(IssuePresenter):
    def _show_issues_table(self, issues: Sequence[Issue]):
        table = Table("Title")

        for issue in issues:
            table.add_row(issue.title)

        console.print(table)

    def select_issue_dialog(self, issues: Sequence[Issue]) -> Issue:
        self._show_issues_table(issues)
        selected_issue_title = questionary.autocomplete(
            "I found these issues for you. Which one do you want to work on?",
            choices=[issue.title for issue in issues],
            qmark="",
        ).ask()

        return next(issue for issue in issues if issue.title == selected_issue_title)
