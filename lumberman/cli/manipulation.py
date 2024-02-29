from typing import TYPE_CHECKING

from rich import print

from lumberman.cli.config import ISSUE_CONTROLLER, STACK_MANIPULATOR, STACK_NAVIGATOR, STACK_OP
from lumberman.cli.location import Location, LocationCLIOption
from lumberman.cli.markdown import print_md
from lumberman.issues.provider import GithubIssue, Issue, RemoteIssue

if TYPE_CHECKING:
    from lumberman.issues.provider import IssueComment


def _markdown_quote_string(string: str) -> str:
    return "\n".join([f"> {line}" for line in string.split("\n")])


def _print_comment(comment: "IssueComment"):
    print_md(f"## {comment.author_login}")
    print_md(_markdown_quote_string(comment.body))


def _select_issue() -> "Issue":
    selected_issue = ISSUE_CONTROLLER.select_issue()
    print_md(f"# {selected_issue.title!s}")

    if isinstance(selected_issue, GithubIssue):
        print_md("## Description")
        description = _markdown_quote_string(selected_issue.description)
        print_md(description)

        if comments := selected_issue.get_comments():
            for comment in comments:
                _print_comment(comment)

    return selected_issue


def insert(location: LocationCLIOption = Location.up):
    """Prompt to create a new item on the current stack. Defaults to creating an item in between the current item and the next item."""
    with STACK_OP(sync_time="exit", sync_pull_requests=False):
        selected_issue = _select_issue()

        if location.to_full_location == Location.trunk:
            STACK_NAVIGATOR.trunk()
        if location.to_full_location == Location.bottom:
            STACK_NAVIGATOR.bottom()
        if location.to_full_location == Location.top:
            STACK_NAVIGATOR.top()
        if location.to_full_location == Location.up:
            pass
        if location.to_full_location == Location.down:
            STACK_NAVIGATOR.down()

        STACK_MANIPULATOR.insert(selected_issue)
        if isinstance(selected_issue, RemoteIssue):
            selected_issue.label("in-progress")
            selected_issue.assign(assignee="@me")


def move():
    """Move the current item to a new location in the stack."""
    with STACK_OP(sync_time="exit", sync_pull_requests=True):
        STACK_MANIPULATOR.move()


def delete():
    """Prompt to delete an item."""
    with STACK_OP(sync_time="exit", sync_pull_requests=False):
        STACK_MANIPULATOR.delete()


def fork(location: LocationCLIOption = Location.bottom):
    """Fork into a new stack and add an item. Defaults to forking from the first item in the current stack."""
    with STACK_OP(sync_time="enter", sync_pull_requests=False):
        selected_issue = _select_issue()

        if location.to_full_location == Location.bottom:
            STACK_NAVIGATOR.bottom()
            STACK_NAVIGATOR.up()
        elif location.to_full_location == Location.top:
            STACK_NAVIGATOR.top()
            STACK_NAVIGATOR.down()
        elif location.to_full_location == Location.up:
            pass  # No need to do anything, already in the correct location
        elif location.to_full_location == Location.down:
            STACK_NAVIGATOR.down()

        STACK_MANIPULATOR.fork(selected_issue)
        if isinstance(selected_issue, RemoteIssue):
            selected_issue.label("in-progress")
            selected_issue.assign(assignee="@me")


def new():
    """Start a new stack on top of trunk."""
    with STACK_OP(sync_time="none", sync_pull_requests=False):
        selected_issue = _select_issue()
        STACK_MANIPULATOR.sync(sync_pull_requests=False)
        STACK_NAVIGATOR.trunk()
        STACK_MANIPULATOR.fork(selected_issue)

        if isinstance(selected_issue, RemoteIssue):
            selected_issue.label("in-progress")
            selected_issue.assign(assignee="@me")


def sync(
    automerge: bool = False, draft: bool = False, squash: bool = False, add_pr_label: bool = True
):
    """Synchronize all state, ensuring the stack is internally in sync, and in sync with the remote. Creates PRs if needed."""
    with STACK_OP(sync_time="none", sync_pull_requests=False):
        STACK_MANIPULATOR.sync(
            automerge=automerge, squash=squash, draft=draft, sync_pull_requests=True
        )

        if add_pr_label:
            current_issue = ISSUE_CONTROLLER.provider.get_current_issue()
            if current_issue:
                current_issue.label("has-pr")
        print(":rocket: [bold green]Stack synced![/bold green]")


if __name__ == "__main__":
    insert()
