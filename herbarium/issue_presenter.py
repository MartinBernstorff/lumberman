from collections.abc import Sequence
from dataclasses import dataclass
from typing import Optional, Protocol

import questionary
import typer
from rich.console import Console

from .issue_service import Issue
from .parse_issue_title import parse_issue_title

console = Console()


class IssuePresenter(Protocol):
    def select_issue_dialog(self, issues: Sequence[Issue]) -> Optional[Issue]:
        ...


@dataclass(frozen=True)
class DefaultIssuePresenter(IssuePresenter):
    manual_prompt: str = "Manual"
    refresh_prompt: str = "Refresh..."

    def _show_entry_dialog(self) -> str:
        return typer.prompt("Title")

    def _show_selection_dialog(self, issues: Sequence[Issue]) -> str:
        issue_titles = [issue.description for issue in issues]
        return questionary.select(
            "What's next? 🚀",
            choices=[self.refresh_prompt, self.manual_prompt, *issue_titles],
            default=issue_titles[0],
        ).ask()

    def select_issue_dialog(self, issues: Sequence[Issue]) -> Optional[Issue]:
        selected_issue_title = self._show_selection_dialog(issues=issues)

        if selected_issue_title == self.refresh_prompt:
            return None

        if selected_issue_title == self.manual_prompt:
            selected_issue_title = self._show_entry_dialog()
            parsed_title = parse_issue_title(selected_issue_title)
            return Issue(
                entity_id=None, prefix=parsed_title.prefix, description=parsed_title.description
            )

        return next(issue for issue in issues if issue.description == selected_issue_title)
