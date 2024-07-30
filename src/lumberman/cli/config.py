from lumberman.change_manager.manager import GithubForge, GitLocalManager, LocalAndForge

from ..issues.controller import IssueController
from ..issues.provider import GithubIssueProvider
from ..issues.selecter import DefaultIssueSelecter
from ..issues.stringifyer import DefaultIssueStringifyer
from ..stack.manipulator import GraphtieManager
from ..stack.navigator import GraphiteNavigator
from .interface_elements import QueueOperation

MANAGER = LocalAndForge(
    forge=GithubForge(), local_manager=GitLocalManager(stringifyer=DefaultIssueStringifyer())
)
STACK_NAVIGATOR = GraphiteNavigator()
ISSUE_CONTROLLER = IssueController(
    provider=GithubIssueProvider(), view=DefaultIssueSelecter(), in_progress_label="in-progress"
)
STACK_OP = QueueOperation(
    sync_time="enter", stack_manipulator=MANAGER, stack_navigator=STACK_NAVIGATOR
)
