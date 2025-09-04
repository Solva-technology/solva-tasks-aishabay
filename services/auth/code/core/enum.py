from enum import Enum


class UserRole(str, Enum):
    student = "student"
    teacher = "teacher"
    manager = "manager"
    admin = "admin"
