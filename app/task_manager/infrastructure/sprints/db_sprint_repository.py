from datetime import date
from typing import Optional, List
from uuid import UUID

from django.db.models import Q

from task_manager.domain.sprint.sprint import Sprint
from task_manager.domain.sprint.sprint_repository import SprintRepository


class DbSprintRepository(SprintRepository):
    def filter_sprint_by_id (self, sprint_id: UUID) -> Optional[Sprint]:
        sprint = Sprint.objects.filter(id=sprint_id).first()
        return sprint

    def filter_sprint(self, company_id: Optional[UUID] = None,  sprint_id: Optional[UUID] = None, name: Optional[str] = None,
             start_date: Optional[date] = None, end_date: Optional[date] = None, objective: Optional[str] = None, active: Optional[bool] = None) -> List[Sprint]:
        filters = Q()
        if sprint_id is not None:
            filters = filters & Q(id=sprint_id)
        if company_id is not None:
            filters = filters & Q(company_id=company_id)
        if name is not None:
            filters = filters & Q(name=name)
        if start_date is not None:
            filters = filters & Q(start_date=start_date)
        if end_date is not None:
            filters = filters & Q(end_date=end_date)
        if objective is not None:
            filters = filters & Q(objective=objective)
        if active is not None:
            filters = filters & Q(active=active)

        sprints = Sprint.objects.filter(filters)
        return sprints


    def save_sprint(self, sprint: Sprint) -> None:
        sprint.save()
