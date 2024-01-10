from collections.abc import Sequence
from types import TracebackType

import typer
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm

from .issue_service import Issue
from .registry import issue_services, presenters, stackers

app = typer.Typer()

issue_service = issue_services["Github"]()
issue_presenter = presenters["Default"]()
stacker = stackers["Graphite"]()

from dataclasses import dataclass


@dataclass
class QueueOperation:
    sync_on_enter: bool = True

    def __enter__(self):
        print(":arrows_clockwise: [bold green]Syncing with remote...[/bold green]")
        if self.sync_on_enter:
            stacker.sync()

    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: TracebackType) -> None:
        stacker.status()


def retry_issue_getting() -> bool:
    retry = Confirm.ask(
        ":palm_tree: No issues assigned to you in this repository. Do you want to retry?",
        default=True,
    )
    return retry


def get_my_issues() -> Sequence[Issue]:
    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True
    ) as progress:
        progress.add_task("Getting issues assigned to you", start=True)
        my_issues = issue_service.get_issues_assigned_to_me()

    if not my_issues:
        if retry_issue_getting():
            next()
        return []

    return my_issues


def select_issue() -> Issue:
    my_issues = get_my_issues()
    selected_issue = issue_presenter.select_issue_dialog(my_issues)

    while selected_issue is None:
        my_issues = get_my_issues()
        selected_issue = issue_presenter.select_issue_dialog(my_issues)

    return selected_issue


@app.command()
def new():
    with QueueOperation():
        selected_issue = select_issue()
        stacker.create_queue_from_trunk(selected_issue)


@app.command()
def insert_at_front():
    with QueueOperation():
        selected_issue = select_issue()
        stacker.add_to_beginning_of_queue(selected_issue)


@app.command()
def next():  # noqa: A001 [Shadowing python built-in]
    with QueueOperation():
        selected_issue = select_issue()
        stacker.add_to_end_of_queue(selected_issue)


@app.command()
def status():
    stacker.status()


@app.command()
def submit(automerge: bool = False):
    with QueueOperation(sync_on_enter=False):
        stacker.submit_queue(automerge=automerge)
        print(":rocket: [bold green]Stack submitted![/bold green]")


if __name__ == "__main__":
    app()
