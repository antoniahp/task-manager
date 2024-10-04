from uuid import UUID

from task_manager.domain.status_column.status_column import StatusColumn


class StatusColumnCreator:
    def status_column_creator(self, status_column_id: UUID, name:str, company_id:UUID) -> StatusColumn:
        return StatusColumn(
            id=status_column_id,
            name=name,
            company_id=company_id
        )
