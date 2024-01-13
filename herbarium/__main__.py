import enum
from collections.abc import Sequence
from types import TracebackType

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
            raise NotImplementedError
        return []

    return my_issues


def select_issue() -> Issue:
    my_issues = get_my_issues()
    selected_issue = issue_presenter.select_issue_dialog(my_issues)

    while selected_issue is None:
        my_issues = get_my_issues()
        selected_issue = issue_presenter.select_issue_dialog(my_issues)

    return selected_issue


class Location(str, enum.Enum):
    front = "front"
    before = "before"
    after = "after"
    back = "back"


class NoOp:
    def __call__(self):
        pass


str2navigation = {
    "front": queue_navigator.go_to_front,
    "before": queue_navigator.move_up_one,
    "after": NoOp(),
    "back": queue_navigator.go_to_back,
}


@app.command()
@app.command(name="a")
@app.command(name="next")
def add(location: Location = Location.after, skip_sync: bool = False):
    with QueueOperation(sync_on_enter=not skip_sync):
        selected_issue = select_issue()
        str2navigation[location.value]()
        queue_manipulator.add(selected_issue)
        issue_service.label_issue(selected_issue, label=in_progress_label)


@app.command()
@app.command(name="f")
@app.command(name="new")
def fork(location: Location = Location.front):
    with QueueOperation():
        selected_issue = select_issue()
        str2navigation[location.value]()
        queue_manipulator.fork(selected_issue)
        issue_service.label_issue(selected_issue, label=in_progress_label)


@app.command()
def status():
    queue_navigator.status()


@app.command()
def submit(automerge: bool = False):
    with QueueOperation(sync_on_enter=False):
        queue_manipulator.submit(automerge=automerge)
        print(":rocket: [bold green]Stack submitted![/bold green]")


if __name__ == "__main__":
    app()
