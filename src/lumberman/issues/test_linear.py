from unittest.mock import patch

import pytest

from .linear import LinearIssue, LinearIssueProvider
from .title_parser import IssueTitle


class TestLinearIssue:
    def _make_issue(self, **kwargs) -> LinearIssue:
        defaults = {
            "entity_id": "abc-123",
            "title": IssueTitle(prefix="feat", content="add login"),
            "description": "A description",
            "identifier": "TEAM-42",
            "labels": [],
        }
        defaults.update(kwargs)
        return LinearIssue(**defaults)

    def test_issue_magic_identifier(self):
        issue = self._make_issue()
        assert issue.issue_magic_identifier() == "TEAM-42"

    def test_branch_id(self):
        issue = self._make_issue()
        assert issue.branch_id() == "TEAM-42"

    def test_render(self):
        issue = self._make_issue()
        assert issue.render() == "TEAM-42: add login"

    def test_get_comments_empty_entity_id(self):
        issue = self._make_issue(entity_id="")
        assert issue.get_comments() == []


class TestLinearIssueProviderValuesToIssue:
    def test_values_to_issue(self):
        provider = LinearIssueProvider()
        node = {
            "id": "issue-id-1",
            "identifier": "PROJ-10",
            "title": "feat: add dark mode",
            "description": "Support dark mode",
        }
        issue = provider._values_to_issue(node)
        assert issue.entity_id == "issue-id-1"
        assert issue.identifier == "PROJ-10"
        assert issue.title.prefix == "feat"
        assert issue.title.content == "add dark mode"
        assert issue.description == "Support dark mode"

    def test_values_to_issue_missing_description(self):
        provider = LinearIssueProvider()
        node = {"id": "id-2", "identifier": "PROJ-11", "title": "fix: typo"}
        issue = provider._values_to_issue(node)
        assert issue.description == ""

    def test_values_to_issue_null_description(self):
        provider = LinearIssueProvider()
        node = {
            "id": "id-3",
            "identifier": "PROJ-12",
            "title": "chore: cleanup",
            "description": None,
        }
        issue = provider._values_to_issue(node)
        assert issue.description == ""


class TestLinearIssueProviderGetCurrentIssue:
    def test_get_current_issue_valid_branch(self):
        provider = LinearIssueProvider()
        with patch("lumberman.issues.linear.shell_output", return_value="feat/TEAM-99/add-feature"):
            issue = provider.get_current_issue()
        assert issue is not None
        assert issue.identifier == "TEAM-99"
        assert issue.title.prefix == "feat"
        assert issue.title.content == "add-feature"
        assert issue.entity_id == ""

    def test_get_current_issue_invalid_branch(self):
        provider = LinearIssueProvider()
        with patch("lumberman.issues.linear.shell_output", return_value="main"):
            issue = provider.get_current_issue()
        assert issue is None

    def test_get_current_issue_two_segments(self):
        provider = LinearIssueProvider()
        with patch("lumberman.issues.linear.shell_output", return_value="feat/some-branch"):
            issue = provider.get_current_issue()
        assert issue is None


class TestLinearIssueProviderIntegration:
    """Integration tests that call the real Linear API.

    These require LINEAR_API_KEY to be set in the environment.
    """

    @pytest.fixture(autouse=True)
    def _require_api_key(self, monkeypatch):
        import os

        key = os.environ.get("LINEAR_API_KEY")
        if not key:
            pytest.skip("LINEAR_API_KEY not set")

    def test_get_latest_issues(self):
        provider = LinearIssueProvider()
        issues = provider.get_latest_issues(in_progress_label="In Progress")
        assert isinstance(issues, list)
        for issue in issues:
            assert isinstance(issue, LinearIssue)
            assert issue.entity_id
            assert issue.identifier

    def test_get_issues_assigned_to_me(self):
        provider = LinearIssueProvider()
        issues = provider.get_issues_assigned_to_me(in_progress_label="In Progress")
        assert isinstance(issues, list)
        for issue in issues:
            assert isinstance(issue, LinearIssue)

    def test_label_issue(self):
        provider = LinearIssueProvider()
        issues = provider.get_latest_issues(in_progress_label="In Progress")
        assert issues, "Need at least one issue to test labeling"
        issue = issues[0]
        issue.label("lumberman-test")

        fetched = provider.get_by_identifier(issue.identifier)
        assert fetched is not None
        assert fetched.labels is not None
