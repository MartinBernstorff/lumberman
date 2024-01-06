import typer

from .registry import issue_services, presenters, stackers

app = typer.Typer()

issue_service = issue_services["Github"]()
issue_presenter = presenters["Default"]()
stacker = stackers["Graphite"]()


@app.command()
def new():
    my_issues = issue_service.get_issues_assigned_to_me()
    selected_issue = issue_presenter.select_issue_dialog(my_issues)
    stacker.create_stack_from_trunk(selected_issue)


@app.command()
def next():  # noqa: A001 [Shadowing python built-in]
    my_issues = issue_service.get_issues_assigned_to_me()
    selected_issue = issue_presenter.select_issue_dialog(my_issues)
    stacker.add_to_stack(selected_issue)


@app.command()
def submit():
    stacker.submit_stack()


if __name__ == "__main__":
    app()
