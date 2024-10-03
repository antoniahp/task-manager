from abc import ABC, abstractmethod
from datetime import date
from typing import Optional, List
from uuid import UUID

from django.db.models import Q

from task_manager.domain.project.project import Project
from task_manager.domain.project.project_repository import ProjectRepository



class DbProjectRepository(ProjectRepository):

    def filtered_project_by_id(self, project_id: Optional[UUID]) -> Optional[Project]:
        project = Project.objects.filter(id=project_id).first()
        return project

    def filtered_projects(self, project_id: Optional[UUID], name: Optional[str] = None, start_date__gte:Optional[date]= None, end_date__lte:Optional[date]= None) -> List[Project]:
        filters = Q()
        if project_id is not None:
            filters = filters & Q(id=project_id)
        if name is not None:
            filters = filters & Q(name=name)
        if start_date__gte is not None:
            filters = filters & Q(start_date__gte=start_date__gte)
        if end_date__lte is not None:
            filters = filters & Q(end_date__lte=end_date__lte)

        projects = Project.objects.filter(filters)
        return projects


    def save_project(self, project: Project) -> None:
        project.save()
