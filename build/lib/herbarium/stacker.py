from typing import Protocol

from .issue_service import Issue
from .subprocess_utils import shell


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

    def submit_stack(self):
        ...


class Graphite(Stacker):
    def create_stack_from_trunk(self, issue: Issue):
        shell("git checkout main")
        shell("git pull")
        self.add_to_stack(issue)

    def add_to_stack(self, issue: Issue):
        sanitised_title = sanitise_issue_title(issue.title)
        branch_title = f"{issue.entity_id}-{sanitised_title}"
        first_commit_str = f"$'{issue.title}\n\nFixes #{issue.entity_id}'"
        shell(f"gt create {branch_title} --all -m {first_commit_str}")
        shell(f"git commit --allow-empty -m {first_commit_str}")

    def submit_stack(self):
        shell("gt submit -m --no-edit --publish")
        shell("gt log short")