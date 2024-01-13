from typing import Protocol

from .issue_parser import IssueParser


class QueueManipulator(Protocol):
    issue_parser: IssueParser

    def fork(self):
        ...

    def add(self):
        ...


class GraphiteManipulator(QueueManipulator):
    issue_parser: IssueParser

    def fork(self):
        ...

    def add(self):
        ...
        # Handle base case

        # Handle insertion case
