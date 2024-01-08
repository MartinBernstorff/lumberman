import typer
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn

from .registry import issue_services, presenters, stackers

app = typer.Typer()

issue_service = issue_services["Github"]()
issue_presenter = presenters["Default"]()
stacker = stackers["Graphite"]()


@app.command()
def new():
    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True
    ) as progress:
        progress.add_task("Getting issues assigned to you", start=True)
        my_issues = issue_service.get_issues_assigned_to_me()
    selected_issue = issue_presenter.select_issue_dialog(my_issues)
    stacker.create_stack_from_trunk(selected_issue)


@app.command()
def next():  # noqa: A001 [Shadowing python built-in]
    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True
    ) as progress:
        progress.add_task("Getting issues assigned to you", start=True)
        my_issues = issue_service.get_issues_assigned_to_me()

    selected_issue = issue_presenter.select_issue_dialog(my_issues)
    stacker.add_to_stack(selected_issue)


@app.command()
def submit(automerge: bool = False):
    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description} "), transient=True
    ) as progress:
        progress.add_task("Submitting stack", start=True)
        stacker.submit_stack(automerge=automerge)
        print(":rocket: [bold green]Stack submitted![/bold green]")


if __name__ == "__main__":
    app()
