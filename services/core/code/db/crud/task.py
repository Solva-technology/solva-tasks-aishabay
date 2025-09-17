import logging

from services.core.code.db.crud.base import CRUDBase
from services.core.code.db.models import Task


logger = logging.getLogger(__name__)


class CRUDTask(CRUDBase):
    pass


task_crud = CRUDTask(Task)
