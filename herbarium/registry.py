from herbarium import queue_manipulator

from .issue_presenter import DefaultIssuePresenter, IssuePresenter
from .issue_service import GithubIssueService, IssueService
from .queue_navigator import GraphiteNavigator, QueueNavigator

issue_services: dict[str, type[IssueService]] = {"Github": GithubIssueService}

queue_navigators: dict[str, type[QueueNavigator]] = {"Graphite": GraphiteNavigator}
queue_manipulators: dict[str, type[queue_manipulator.QueueManipulator]] = {
    "Graphite": queue_manipulator.GraphiteManipulator
}

presenters: dict[str, type[IssuePresenter]] = {"Default": DefaultIssuePresenter}
