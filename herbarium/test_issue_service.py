import pytest

from .issue_service import GithubIssueService


@pytest.mark.skip()
def test_issue_service():
    service = GithubIssueService()
    service.get_issues_assigned_to_me(in_progress_label="in progress")
