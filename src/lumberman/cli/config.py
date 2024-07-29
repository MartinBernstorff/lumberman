from ..issues.controller import IssueController
from ..issues.provider import GithubIssueProvider
from ..issues.selecter import DefaultIssueSelecter
from ..issues.stringifyer import DefaultIssueStringifyer
from ..stack.manipulator import GraphiteManipulator
from ..stack.navigator import GraphiteNavigator
from .interface_elements import QueueOperation

STACK_MANIPULATOR = GraphiteManipulator(issue_parser=DefaultIssueStringifyer())
STACK_NAVIGATOR = GraphiteNavigator()
ISSUE_CONTROLLER = IssueController(
    provider=GithubIssueProvider(), view=DefaultIssueSelecter(), in_progress_label="in-progress"
)
STACK_OP = QueueOperation(
    sync_time="enter", stack_manipulator=STACK_MANIPULATOR, stack_navigator=STACK_NAVIGATOR
)
