from ..issues.controller import IssueController
from ..issues.model import GithubIssueModel
from ..issues.stringifyer import DefaultIssueStringifyer
from ..issues.view import DefaultIssueView
from ..queue.manipulator import GraphiteManipulator
from ..queue.navigator import GraphiteNavigator
from .interface_elements import QueueOperation

QUEUE_MANIPULATOR = GraphiteManipulator(issue_parser=DefaultIssueStringifyer())
QUEUE_NAVIGATOR = GraphiteNavigator()
ISSUE_CONTROLLER = IssueController(
    model=GithubIssueModel(), view=DefaultIssueView(), in_progress_label="in-progress"
)
QUEUE_OP = QueueOperation(
    sync_time="enter", queue_manipulator=QUEUE_MANIPULATOR, queue_navigator=QUEUE_NAVIGATOR
)
