from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, Union

import typer
from iterfzf import iterfzf  # type: ignore
from rich.console import Console

from .provider import Issue
from .title_parser import parse_issue_title

if TYPE_CHECKING:
    from collections.abc import Sequence

console = Console()


class IssueSelecter(Protocol):
    ten_latest_prompt: str
    refresh_prompt: str

    def select_issue_dialog(self, issues: "Sequence[Issue]") -> Union[Issue, str]:
        ...


@dataclass(frozen=True)
class FZFSelection:
    input_str: str
    selected_str: str

    def any_string(self) -> str:
        return self.selected_str or self.input_str


@dataclass(frozen=True)
class DefaultIssueSelecter(IssueSelecter):
    ten_latest_prompt: str = "Recent"
    refresh_prompt: str = "Refresh..."

    def _show_selection_dialog(self, issues: "Sequence[Issue]") -> FZFSelection:
        issue_titles = [f"{issue.title.content} #{issue.entity_id}" for issue in issues]
        typer.echo("Select an issue or enter a new issue title.")
        selection: tuple(str, str) = iterfzf([*issue_titles, self.refresh_prompt], print_query=True)  # type: ignore
        return FZFSelection(input_str=selection[0], selected_str=selection[1])  # type: ignore

    def select_issue_dialog(self, issues: "Sequence[Issue]") -> Union[Issue, str]:
        selected_issue = self._show_selection_dialog(issues=issues)
        selected_issue_title = selected_issue.any_string()

        if selected_issue_title in [self.refresh_prompt]:
            return selected_issue_title

        selected_issue_from_list = [i for i in issues if i.title.content == selected_issue_title]
        if selected_issue_from_list:
            return next(issue for issue in selected_issue_from_list)

        parsed_title = parse_issue_title(selected_issue_title)
        return Issue(entity_id=None, title=parsed_title, description="")
