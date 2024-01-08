from collections.abc import Sequence
from typing import Optional, Protocol

import questionary
from rich.console import Console

from .issue_service import Issue

console = Console()


class IssuePresenter(Protocol):
    def select_issue_dialog(self, issues: Sequence[Issue], refresh_prompt: str) -> Optional[Issue]:
        ...


class DefaultIssuePresenter(IssuePresenter):
    def _show_dialog(self, issues: Sequence[Issue], refresh_prompt: str) -> Optional[str]:
        issue_titles = [issue.title for issue in issues]
        return questionary.select(
            "I found these issues for you. Which one do you want to work on?",
            choices=[refresh_prompt, *issue_titles],
            default=issue_titles[0],
            qmark="",
        ).ask()

    def select_issue_dialog(self, issues: Sequence[Issue], refresh_prompt: str) -> Optional[Issue]:
        selected_issue_title = self._show_dialog(issues=issues, refresh_prompt=refresh_prompt)
        if selected_issue_title == refresh_prompt:
            return None

        return next(issue for issue in issues if issue.title == selected_issue_title)
