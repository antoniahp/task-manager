from typing import Optional
from uuid import UUID

from django.db.models import Q

from task_manager.domain.status_column.status_column import StatusColumn
from task_manager.domain.status_column.status_column_repository import StatusColumnRepository


class DbStatusColumnRepository(StatusColumnRepository):

    def filter_status_column_by_id(self, status_column_id: UUID) -> Optional[StatusColumn]:
        status_column = StatusColumn.objects.filter(id=status_column_id).first()
        return status_column

    def filter_status_columns(self, status_column_id: Optional[UUID], name: Optional[str], company_id: Optional[UUID], order: Optional[int]) -> Optional[StatusColumn]:
        filters = Q()
        if status_column_id is not None:
            filters = filters & Q(id=status_column_id)
        if name is not None:
            filters = filters & Q(name=name)
        if company_id is not None:
            filters = filters & Q(company_id=company_id)
        if order is not None:
            filters = filters & Q(order=order)

        status_column = StatusColumn.objects.filter(filters)
        return status_column


    def save_status_column(self, status_column: StatusColumn):
        status_column.save()
