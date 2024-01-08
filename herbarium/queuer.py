import re
from dataclasses import dataclass
from typing import Protocol

from .issue_service import Issue
from .subprocess_utils import interactive_cmd


@dataclass(frozen=True)
class ParsedIssue:
    prefix: str
    description: str


def sanitise_text_for_git(input_string: str) -> str:
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
        input_string = input_string.replace(character, replacement)

    return input_string.replace("--", "-")


def parse_issue_title(issue_title: str) -> ParsedIssue:
    # Get all string between start and first ":"
    prefix = re.findall(r"^(.*?):", issue_title)[0]
    description = re.findall(r": (.*)$", issue_title)[0]

    return ParsedIssue(
        prefix=sanitise_text_for_git(input_string=prefix),
        description=sanitise_text_for_git(input_string=description),
    )


class Queuer(Protocol):
    def create_queue_from_trunk(self, issue: Issue):
        ...

    def add_to_end_of_queue(self, issue: Issue):
        ...

    def submit_queue(self, automerge: bool):
        ...

    def status(self):
        ...


class Graphite(Queuer):
    def _sync(self):
        interactive_cmd("gt sync --force")

    def create_queue_from_trunk(self, issue: Issue):
        self._sync()
        interactive_cmd("git checkout main")
        interactive_cmd("git pull")
        self.add_to_end_of_queue(issue)

    def add_to_end_of_queue(self, issue: Issue):
        self._sync()
        parsed_issue = parse_issue_title(issue.title)

        entity_id_section = "" if issue.entity_id is None else f"/{issue.entity_id}"
        branch_title = f"{parsed_issue.prefix}{entity_id_section}/{parsed_issue.description}"

        first_commit_str = f"{issue.title}"
        if issue.entity_id is not None:
            first_commit_str += "\n\nFixes #{issue.entity_id}"

        interactive_cmd(f'gt create {branch_title} --all -m "{first_commit_str}"')
        interactive_cmd(f'git commit --allow-empty -m "{first_commit_str}"')

    def submit_queue(self, automerge: bool):
        self._sync()
        submit_command = "gt submit --no-edit --publish"

        if automerge:
            submit_command += " --merge-when-ready"

        interactive_cmd(submit_command)

    def status(self):
        interactive_cmd("gt log short --reverse")