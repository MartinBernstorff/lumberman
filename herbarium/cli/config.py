from ..issues.controller import IssueController
from ..issues.model import GithubIssueModel
from ..issues.stringifyer import DefaultIssueStringifyer
from ..issues.view import DefaultIssueView
from ..stack.manipulator import GraphiteManipulator
from ..stack.navigator import GraphiteNavigator
from .interface_elements import QueueOperation

STACK_MANIPULATOR = GraphiteManipulator(issue_parser=DefaultIssueStringifyer())
STACK_NAVIGATOR = GraphiteNavigator()
ISSUE_CONTROLLER = IssueController(
    model=GithubIssueModel(), view=DefaultIssueView(), in_progress_label="in-progress"
)
STACK_OP = QueueOperation(
    sync_time="enter", stack_manipulator=STACK_MANIPULATOR, stack_navigator=STACK_NAVIGATOR
)
