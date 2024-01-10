from typing import Protocol

from herbarium.parse_issue_title import sanitise_text_for_bash

from .git_utils import StagingMigrater
from .issue_service import Issue
from .subprocess_utils import interactive_cmd


class Queuer(Protocol):
    def sync(self):
        ...

    def create_queue_from_trunk(self, issue: Issue):
        ...

    def add_to_beginning_of_queue(self, issue: Issue):
        ...

    def add_to_end_of_queue(self, issue: Issue):
        ...

    def submit_queue(self, automerge: bool):
        ...

    def status(self):
        ...


class Graphite(Queuer):
    def sync(self):
        interactive_cmd("gt sync --force --restack")

    def create_queue_from_trunk(self, issue: Issue):
        with StagingMigrater():
            interactive_cmd("gt trunk")
        self.add_to_end_of_queue(issue)

    def add_to_beginning_of_queue(self, issue: Issue):
        first_commit_str = self._get_first_commit_str(issue)
        branch_title = self._get_branch_title(issue=issue)

        with StagingMigrater():
            interactive_cmd("gt bottom")

        interactive_cmd("gt trunk")
        interactive_cmd(f'gt create {branch_title} --all --insert -m "{first_commit_str}"')
        interactive_cmd(f'git commit --allow-empty -m "{first_commit_str}"')

    def add_to_end_of_queue(self, issue: Issue):
        first_commit_str = self._get_first_commit_str(issue)
        branch_title = self._get_branch_title(issue=issue)

        interactive_cmd(f'gt create {branch_title} --all -m "{first_commit_str}"')
        interactive_cmd(f'git commit --allow-empty -m "{first_commit_str}"')

    def _get_first_commit_str(self, issue: Issue) -> str:
        if issue.entity_id is None:
            first_commit_str = f"{issue.prefix}: {issue.description}"
        else:
            first_commit_str = f"""{issue.prefix}(#{issue.entity_id}): {issue.description}

Fixes #{issue.entity_id}"""

        return sanitise_text_for_bash(first_commit_str)

    def _get_branch_title(self, issue: Issue) -> str:
        entity_id_section = "" if issue.entity_id is None else f"/{issue.entity_id}"
        return f"{issue.prefix}{entity_id_section}/{issue.description}"

    def submit_queue(self, automerge: bool):
        submit_command = "gt submit --no-edit --publish --stack"

        if automerge:
            submit_command += " --merge-when-ready"

        interactive_cmd(submit_command)

    def status(self):
        interactive_cmd("gt log short --reverse")
