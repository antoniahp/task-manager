from datetime import date
from uuid import UUID

from task_manager.domain.project.project import Project


class ProjectCreator:
    def create_project(self, project_id: UUID, name: str, start_date: date, end_date:date, company_id: UUID) -> Project:
        return Project(
            id=project_id,
            name=name,
            start_date=start_date,
            end_date=end_date,
            company_id=company_id
        )