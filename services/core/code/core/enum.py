from enum import Enum


class TaskStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in progress"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
