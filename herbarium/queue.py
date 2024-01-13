from typing import Protocol

from .queue_manipulator import QueueManipulator
from .queue_navigator import QueueNavigator


class Queue(Protocol):
    navigator: QueueNavigator
    manipulator: QueueManipulator
