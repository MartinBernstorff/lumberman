from collections.abc import Sequence
from types import TracebackType
from typing import Literal

import typer
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm

from .issue_service import Issue
from .registry import issue_services, presenters, queue_manipulators, queue_navigators

app = typer.Typer()

issue_service = issue_services["Github"]()
issue_presenter = presenters["Default"]()
queue_navigator = queue_navigators["Graphite"]()
queue_manipulator = queue_manipulators["Graphite"]()

from dataclasses import dataclass


@dataclass
class QueueOperation:
    sync_on_enter: bool = True

    def __enter__(self):
        print(":arrows_clockwise: [bold green]Syncing with remote...[/bold green]")
        if self.sync_on_enter:
            queue_manipulator.sync()

    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: TracebackType) -> None:
        queue_navigator.status()


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


LocationType = Literal["front", "before", "after", "back"]

str2navigation = {
    "front": queue_navigator.go_to_front,
    "before": queue_navigator.move_up_one,
    "after": queue_navigator.move_down_one,
    "back": queue_navigator.go_to_back,
}


@app.command()
def add(location: LocationType):
    with QueueOperation():
        selected_issue = select_issue()
        str2navigation[location]()
        queue_manipulator.add(selected_issue)
        print(
            f":heavy_plus_sign: [bold green]Issue {selected_issue} added to the queue![/bold green]"
        )


@app.command()
def fork(location: LocationType):
    with QueueOperation():
        selected_issue = select_issue()
        str2navigation[location]()
        queue_manipulator.fork(selected_issue)
        print(f":fork_and_knife: [bold green]Issue {selected_issue} forked![/bold green]")


@app.command()
def status():
    queue_navigator.status()


@app.command()
def submit(automerge: bool = False):
    with QueueOperation(sync_on_enter=False):
        queue_navigator.submit_queue(automerge=automerge)
        print(":rocket: [bold green]Stack submitted![/bold green]")


if __name__ == "__main__":
    app()
