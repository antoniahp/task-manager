from datetime import date
from uuid import UUID
from task_manager.domain.sprint.sprint import Sprint


class SprintCreator:
    def create_sprint(self, sprint_id: UUID, name:str, objective:str, start_date: date, end_date: date, active: bool, company_id: UUID ) -> Sprint:
        return Sprint(
            id=sprint_id,
            name=name,
            objective=objective,
            start_date=start_date,
            end_date=end_date,
            active=active,
            company_id=company_id
        )
