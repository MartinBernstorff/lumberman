from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

import typer
from iterfzf import iterfzf  # type: ignore
from rich.console import Console

from .provider import GithubIssue, Issue, LocalIssue
from .title_parser import parse_issue_title

if TYPE_CHECKING:
    from collections.abc import Sequence

console = Console()


class IssueSelecter(Protocol):
    def select_issue_dialog(self, issues: "Sequence[GithubIssue]") -> Issue:
        ...


@dataclass(frozen=True)
class FZFSelection:
    input_str: str  # String typed into FZF dialog
    selected_str: str | None  # Selected string from FZF, e.g. the matching entry

    def either(self) -> str:
        return self.selected_str or self.input_str


@dataclass(frozen=True)
class DefaultIssueSelecter(IssueSelecter):
    def _show_selection_dialog(self, issues: "Sequence[GithubIssue]") -> FZFSelection:
        issue_titles = [f"{issue.title.content} #{issue.entity_id}" for issue in issues]
        if len(issue_titles) == 0:
            issue_titles.append("No issues found. Enter an title for the change below.")

        typer.echo("Select an issue or enter a new issue title.")
        selection: tuple(str, str) = iterfzf([*issue_titles], print_query=True, exact=True)  # type: ignore
        return FZFSelection(input_str=selection[0], selected_str=selection[1])  # type: ignore

    def select_issue_dialog(self, issues: "Sequence[GithubIssue]") -> Issue:
        fzf_selection = self._show_selection_dialog(issues=issues)
        selected_issue_title = fzf_selection.either()

        selected_issue_from_list = [i for i in issues if i.title.content in selected_issue_title]
        if selected_issue_from_list:
            return next(issue for issue in selected_issue_from_list)

        parsed_title = parse_issue_title(selected_issue_title)
        return LocalIssue(title=parsed_title)
