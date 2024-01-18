import pytest

from .model import GithubIssueModel


@pytest.mark.skip()
def test_issue_model():
    service = GithubIssueModel()
    service.get_issues_assigned_to_me(in_progress_label="in progress")
