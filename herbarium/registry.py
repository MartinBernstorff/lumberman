from .issue_presenter import DefaultIssuePresenter, IssuePresenter
from .issue_service import GithubIssueService, IssueService
from .queuer import Graphite, Queuer

issue_services: dict[str, type[IssueService]] = {"Github": GithubIssueService}
stackers: dict[str, type[Queuer]] = {"Graphite": Graphite}
presenters: dict[str, type[IssuePresenter]] = {"Default": DefaultIssuePresenter}
