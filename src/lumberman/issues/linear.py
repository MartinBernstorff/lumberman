import json
from dataclasses import dataclass
from typing import TYPE_CHECKING

from lumberman.cli.subprocess_utils import shell_output
from lumberman.issues.provider import Issue, IssueComment, RemoteIssue
from lumberman.issues.title_parser import IssueTitle, parse_issue_title

if TYPE_CHECKING:
    from collections.abc import Sequence


def _linear_api(query: str) -> dict:
    escaped = query.replace('"', '\\"').replace("\n", "\\n")
    result = shell_output(
        f"curl -s -X POST https://api.linear.app/graphql "
        f'-H "Content-Type: application/json" '
        f'-H "Authorization: $LINEAR_API_KEY" '
        f'-d \'{{"query": "{escaped}"}}\''
    )
    if result is None:
        return {}
    return json.loads(result)


@dataclass
class LinearIssue(RemoteIssue, Issue):
    entity_id: str
    title: IssueTitle
    description: str
    identifier: str  # e.g. "TEAM-123"
    labels: Sequence[str]

    def issue_magic_identifier(self) -> str:
        return f"{self.identifier}"

    def branch_id(self) -> str:
        return self.identifier

    def render(self) -> str:
        return f"{self.identifier}: {self.title.content}"

    def label(self, label: str) -> None:
        # Find or create the label, then attach it
        result = _linear_api(f"""
            mutation {{
                issueLabelCreate(input: {{ name: "{label}" }}) {{
                    issueLabel {{ id }}
                }}
            }}
        """)
        try:
            label_id = result["data"]["issueLabelCreate"]["issueLabel"]["id"]
        except (KeyError, TypeError):
            # Label may already exist; search for it
            result = _linear_api(f"""
                {{
                    issueLabels(filter: {{ name: {{ eq: "{label}" }} }}) {{
                        nodes {{ id }}
                    }}
                }}
            """)
            try:
                label_id = result["data"]["issueLabels"]["nodes"][0]["id"]
            except (KeyError, TypeError, IndexError) as e:
                raise RuntimeError(f"Error finding/creating label {label}") from e

        _linear_api(f"""
            mutation {{
                issueUpdate(id: "{self.entity_id}", input: {{ labelIds: ["{label_id}"] }}) {{
                    issue {{ id }}
                }}
            }}
        """)

    def get_comments(self) -> "Sequence[IssueComment]":
        if not self.entity_id:
            return []

        result = _linear_api(f"""
            {{
                issue(id: "{self.entity_id}") {{
                    comments {{
                        nodes {{ id body url user {{ displayName }} }}
                    }}
                }}
            }}
        """)
        try:
            comments = result["data"]["issue"]["comments"]["nodes"]
        except (KeyError, TypeError):
            return []

        return [
            IssueComment(
                id=c["id"],
                body=c["body"],
                url=c.get("url", ""),
                author_login=c.get("user", {}).get("displayName", ""),
            )
            for c in comments
        ]

    def assign_me(self) -> None:
        result = _linear_api("""
            {
                viewer { id }
            }
        """)
        try:
            user_id = result["data"]["viewer"]["id"]
        except (KeyError, TypeError) as e:
            raise RuntimeError("Error finding current user") from e

        _linear_api(f"""
            mutation {{
                issueUpdate(id: "{self.entity_id}", input: {{ assigneeId: "{user_id}" }}) {{
                    issue {{ id }}
                }}
            }}
        """)


class LinearIssueProvider:
    def setup(self) -> None:
        pass

    def _values_to_issue(self, node: dict) -> LinearIssue:
        parsed_title = parse_issue_title(node.get("title", ""))
        label_nodes = node.get("labels", {}).get("nodes", [])
        return LinearIssue(
            entity_id=node["id"],
            identifier=node.get("identifier", ""),
            title=parsed_title,
            description=node.get("description", "") or "",
            labels=[l["name"] for l in label_nodes],
        )

    def get_by_identifier(self, identifier: str) -> LinearIssue | None:
        number = identifier.split("-")[-1]
        result = _linear_api(f"""
            {{
                issues(filter: {{ number: {{ eq: {number} }} }}) {{
                    nodes {{ id identifier title description labels {{ nodes {{ name }} }} }}
                }}
            }}
        """)
        try:
            nodes = result["data"]["issues"]["nodes"]
            if not nodes:
                return None
            return self._values_to_issue(nodes[0])
        except (KeyError, TypeError):
            return None

    def get_latest_issues(self, in_progress_label: str) -> "Sequence[LinearIssue]":
        result = _linear_api(f"""
            {{
                issues(
                    first: 10,
                    filter: {{
                        state: {{ name: {{ neq: "{in_progress_label}" }} }},
                        completedAt: {{ null: true }},
                        canceledAt: {{ null: true }}
                    }},
                    orderBy: createdAt
                ) {{
                    nodes {{ id identifier title description labels {{ nodes {{ name }} }} }}
                }}
            }}
        """)
        nodes = result["data"]["issues"]["nodes"]

        return [self._values_to_issue(n) for n in nodes]

    def get_issues_assigned_to_me(self, in_progress_label: str) -> "Sequence[LinearIssue]":
        result = _linear_api(f"""
            {{
                viewer {{
                    assignedIssues(
                        filter: {{
                            state: {{ name: {{ neq: "{in_progress_label}" }} }},
                            completedAt: {{ null: true }},
                            canceledAt: {{ null: true }}
                        }}
                    ) {{
                        nodes {{ id identifier title description labels {{ nodes {{ name }} }} }}
                    }}
                }}
            }}
        """)
        try:
            nodes = result["data"]["viewer"]["assignedIssues"]["nodes"]
        except (KeyError, TypeError):
            return []

        return [self._values_to_issue(n) for n in nodes]

    def get_current_issue(self) -> LinearIssue | None:
        current_branch: str = shell_output("git rev-parse --abbrev-ref HEAD")  # type: ignore

        branch_items = current_branch.split("/")

        if len(branch_items) != 3:
            return None

        return LinearIssue(
            entity_id="",
            identifier=branch_items[1],
            title=IssueTitle(prefix=branch_items[0], content=branch_items[2]),
            description="",
            labels=[],
        )
