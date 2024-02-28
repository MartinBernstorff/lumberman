from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, Union

import typer
from iterfzf import iterfzf  # type: ignore
from rich.console import Console

from .provider import GithubIssue
from .title_parser import parse_issue_title

if TYPE_CHECKING:
    from collections.abc import Sequence

console = Console()


class IssueSelecter(Protocol):
    def select_issue_dialog(self, issues: "Sequence[GithubIssue]") -> Union[GithubIssue, str]:
        ...


@dataclass(frozen=True)
class FZFSelection:
    input_str: str
    selected_str: str

    def either(self) -> str:
        return self.selected_str or self.input_str


@dataclass(frozen=True)
class DefaultIssueSelecter(IssueSelecter):
    def _show_selection_dialog(self, issues: "Sequence[GithubIssue]") -> FZFSelection:
        issue_titles = [f"{issue.title.content} #{issue.entity_id}" for issue in issues]
        typer.echo("Select an issue or enter a new issue title.")
        selection: tuple(str, str) = iterfzf([*issue_titles], print_query=True)  # type: ignore
        return FZFSelection(input_str=selection[0], selected_str=selection[1])  # type: ignore

    def select_issue_dialog(self, issues: "Sequence[GithubIssue]") -> Union[GithubIssue, str]:
        fzf_selection = self._show_selection_dialog(issues=issues)
        selected_issue_title = fzf_selection.either()

        selected_issue_from_list = [i for i in issues if i.title.content == selected_issue_title]
        if selected_issue_from_list:
            return next(issue for issue in selected_issue_from_list)

        parsed_title = parse_issue_title(selected_issue_title)
        return GithubIssue(entity_id=None, title=parsed_title, description="")
