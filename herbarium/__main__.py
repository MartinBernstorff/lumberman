import enum
from collections.abc import Sequence
from types import TracebackType
from typing import Annotated, Literal, Optional

import typer
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm

from .issue_service import Issue
from .registry import issue_services, presenters, queue_manipulators, queue_navigators

app = typer.Typer()

in_progress_label = "in-progress"
issue_service = issue_services["Github"]()
issue_presenter = presenters["Default"]()
queue_navigator = queue_navigators["Graphite"]()
queue_manipulator = queue_manipulators["Graphite"]

from dataclasses import dataclass


@dataclass
class QueueOperation:
    sync_time: Literal["enter", "exit", "none"] = "enter"

    def __enter__(self):
        print(":arrows_clockwise: [bold green]Syncing with remote...[/bold green]")
        if self.sync_time == "enter":
            queue_manipulator.sync()

    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: TracebackType) -> None:
        if self.sync_time == "exit":
            queue_manipulator.sync()
        queue_navigator.status()


def retry_issue_getting() -> bool:
    retry = Confirm.ask(
        ":palm_tree: No issues assigned to you in this repository. Do you want to retry?",
        default=True,
    )
    return retry


def get_latest_issues() -> Sequence[Issue]:
    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True
    ) as progress:
        progress.add_task("Getting latest issues", start=True)
        latest_issues = issue_service.get_latest_issues(in_progress_label=in_progress_label)

    if not latest_issues:
        return []

    return latest_issues


def get_my_issues() -> Sequence[Issue]:
    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True
    ) as progress:
        progress.add_task("Getting issues assigned to you", start=True)
        my_issues = issue_service.get_issues_assigned_to_me(in_progress_label=in_progress_label)

    return my_issues


def select_issue(issues: Optional[Sequence[Issue]] = None) -> Issue:
    if not issues:
        issues = get_my_issues()
    selected_issue = issue_presenter.select_issue_dialog(issues)

    if selected_issue is issue_presenter.refresh_prompt:
        return select_issue()
    if selected_issue is issue_presenter.ten_latest_prompt:
        return select_issue(get_latest_issues())
    if isinstance(selected_issue, str):
        raise NotImplementedError(f"Command {selected_issue} not implemented")

    return selected_issue


class Location(str, enum.Enum):
    front = "front"
    before = "before"
    after = "after"
    back = "back"


LocationCLIOption = Annotated[Location, typer.Argument()]


@app.command()
@app.command(name="a")
@app.command(name="next")
def add(location: LocationCLIOption = Location.after):
    with QueueOperation(sync_time="exit"):
        selected_issue = select_issue()

        if location == Location.front:
            queue_navigator.go_to_front()
        elif location == Location.back:
            queue_navigator.go_to_back()
        elif location == Location.after:
            pass
        elif location == Location.before:
            queue_navigator.move_forward_one()

        queue_manipulator.add(selected_issue)
        issue_service.label_issue(selected_issue, label=in_progress_label)


@app.command()
@app.command(name="f")
def fork(location: LocationCLIOption = Location.front):
    with QueueOperation(sync_time="exit"):
        selected_issue = select_issue()

        if location == Location.front:
            queue_navigator.go_to_second_in_line()
        elif location == Location.back:
            queue_navigator.go_to_next_to_last()
        elif location == Location.after:
            pass  # No need to do anything, already in the correct location
        elif location == Location.before:
            queue_navigator.move_forward_one()

        queue_manipulator.fork(selected_issue)
        issue_service.label_issue(selected_issue, label=in_progress_label)


@app.command()
def new():
    with QueueOperation(sync_time="exit"):
        selected_issue = select_issue()
        queue_navigator.go_to_front()
        queue_manipulator.fork(selected_issue)
        issue_service.label_issue(selected_issue, label=in_progress_label)


@app.command()
def status():
    queue_navigator.status()


@app.command()
def submit(automerge: bool = False):
    with QueueOperation(sync_time="enter"):
        queue_manipulator.submit(automerge=automerge)
        print(":rocket: [bold green]Stack submitted![/bold green]")


if __name__ == "__main__":
    app()
