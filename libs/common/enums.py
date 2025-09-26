from enum import Enum


class UserRole(str, Enum):
    student = "student"
    teacher = "teacher"
    manager = "manager"
    admin = "admin"


class TaskStatus(str, Enum):
    new = "new"
    in_progress = "in_progress"
    submitted = "submitted"
    accepted = "accepted"
