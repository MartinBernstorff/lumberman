from dataclasses import dataclass

import pytest

from .issue_service import Issue
from .issue_stringifyer import DefaultIssueStringifyer


@dataclass(frozen=True)
class TestIssueStringifyer:
    input_issue: Issue
    first_commit_str: str
    branch_title: str


@pytest.mark.parametrize(
    ("example"),
    [
        TestIssueStringifyer(
            input_issue=Issue(entity_id="42", prefix="test-prefix", description="test-description"),
            first_commit_str="""test-prefix(#42): test-description

Fixes #42""",
            branch_title="test-prefix/42/test-description",
        ),
        TestIssueStringifyer(
            input_issue=Issue(entity_id=None, prefix=None, description="test-description"),
            first_commit_str="""test-description""",
            branch_title="test-description",
        ),
        TestIssueStringifyer(
            input_issue=Issue(entity_id="42", prefix=None, description="test-description"),
            first_commit_str="""(#42): test-description

Fixes #42""",
            branch_title="42/test-description",
        ),
        TestIssueStringifyer(
            input_issue=Issue(entity_id=None, prefix="test-prefix", description="test-description"),
            first_commit_str="""test-prefix: test-description""",
            branch_title="test-prefix/test-description",
        ),
    ],
)
def test_default_issue_stringifyer(example: TestIssueStringifyer):
    issue_info = DefaultIssueStringifyer().get_issue_info(issue=example.input_issue)
    assert issue_info.first_commit_str == example.first_commit_str
    assert issue_info.branch_title == example.branch_title
