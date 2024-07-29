import pytest

from .provider import GithubIssueProvider


@pytest.mark.skip()
def test_issue_model():
    service = GithubIssueProvider()
    service.get_issues_assigned_to_me(in_progress_label="in progress")
