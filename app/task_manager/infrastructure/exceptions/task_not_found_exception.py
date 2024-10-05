from uuid import UUID


class TaskNotFoundException(Exception):
    def __init__(self, task_id: UUID):
        self.task_id = task_id
        self.message = f"Task {task_id} not found"
        super().__init__(self.message)