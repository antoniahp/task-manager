from uuid import UUID


class SprintNotFoundException(Exception):
    def __init__(self, sprint_id: UUID):
        self.sprint_id = sprint_id
        self.message = f"Sprint with ID {sprint_id} not found"
        super().__init__(self.message)