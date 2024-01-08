from typing import Protocol

from .issue_service import Issue
from .subprocess_utils import interactive_cmd


def sanitise_issue_title(issue_title: str) -> str:
    char2replacement = {
        " ": "-",
        ":": "/",
        ",": "",
        "'": "",
        '"': "",
        "(": "",
        ")": "",
        "[": "",
        "": "",
        "`": "",
        ">": "",
        "<": "",
        "=": "",
    }

    for character, replacement in char2replacement.items():
        issue_title = issue_title.replace(character, replacement)

    issue_title = issue_title.replace("--", "-")
    return issue_title


class Stacker(Protocol):
    def create_stack_from_trunk(self, issue: Issue):
        ...

    def add_to_stack(self, issue: Issue):
        ...

    def submit_stack(self, automerge: bool):
        ...

    def status(self):
        ...


class Graphite(Stacker):
    def _sync(self):
        interactive_cmd("gt sync --force --show-delete-progress")

    def create_stack_from_trunk(self, issue: Issue):
        self._sync()
        interactive_cmd("git checkout main")
        interactive_cmd("git pull")
        self.add_to_stack(issue)

    def add_to_stack(self, issue: Issue):
        self._sync()
        sanitised_title = sanitise_issue_title(issue.title)
        branch_title = f"{issue.entity_id}-{sanitised_title}"
        first_commit_str = f"'{issue.title}\n\nFixes #{issue.entity_id}'"
        interactive_cmd(f"gt create {branch_title} --all -m {first_commit_str}")
        interactive_cmd(f"git commit --allow-empty -m {first_commit_str}")

    def submit_stack(self, automerge: bool):
        self._sync()
        submit_command = "gt submit --no-edit --publish"

        if automerge:
            submit_command += " --merge-when-ready"

        interactive_cmd(submit_command)

    def status(self):
        interactive_cmd("gt log short --reverse")
