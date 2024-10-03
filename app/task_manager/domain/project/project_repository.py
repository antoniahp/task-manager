from abc import ABC, abstractmethod
from datetime import date
from typing import Optional, List
from uuid import UUID

from task_manager.domain.project.project import Project


class ProjectRepository(ABC):

    @abstractmethod
    def filtered_project_by_id(self, project_id: Optional[UUID]) -> Project:
        pass
    @abstractmethod
    def filtered_projects(self, project_id: Optional[UUID], name: Optional[str] = None, start_date__gte:Optional[date]= None, end_date__lte:Optional[date]= None) -> List[Project]:
        pass

    @abstractmethod
    def save_project(self, project:Project) -> None:
        pass