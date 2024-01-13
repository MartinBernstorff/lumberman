from herbarium import queue_manipulator

from .issue_parser import DefaultIssueParser
from .issue_presenter import DefaultIssuePresenter, IssuePresenter
from .issue_service import GithubIssueService, IssueService
from .queue_navigator import GraphiteNavigator, QueueNavigator

issue_services: dict[str, type[IssueService]] = {"Github": GithubIssueService}

queue_navigators: dict[str, type[QueueNavigator]] = {"Graphite": GraphiteNavigator}
queue_manipulators: dict[str, queue_manipulator.QueueManipulator] = {
    "Graphite": queue_manipulator.GraphiteManipulator(issue_parser=DefaultIssueParser())
}

presenters: dict[str, type[IssuePresenter]] = {"Default": DefaultIssuePresenter}
