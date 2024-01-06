from .issue_presenter import DefaultIssuePresenter, IssuePresenter
from .issue_service import GithubIssueService, IssueService
from .stacker import Graphite, Stacker

issue_services: dict[str, type[IssueService]] = {"Github": GithubIssueService}
stackers: dict[str, type[Stacker]] = {"Graphite": Graphite}
presenters: dict[str, type[IssuePresenter]] = {"Default": DefaultIssuePresenter}
