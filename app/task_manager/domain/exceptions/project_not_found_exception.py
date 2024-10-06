from uuid import UUID


class ProjectNotFoundException(Exception):
    def __init__(self, project_id: UUID):
        self.project_id = project_id
        self.message = f"Project {project_id} not found"
        super().__init__(self.message)