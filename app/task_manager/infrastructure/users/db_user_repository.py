from typing import Optional
from uuid import UUID

from django.db.models import Q

from task_manager.domain.user.user import User
from task_manager.domain.user.user_repository import UserRepository


class DbUserRepository(UserRepository):
    def filter_user_by_id(self, user_id: UUID) -> Optional[User]:
        user = User.objects.filter(id=user_id).first()
        return user

    def filter_users(self, user_id: Optional[UUID], name: Optional[str], company:Optional[UUID]) -> Optional[User]:
        filters = Q()
        if user_id is not None:
            filters = filters & Q(id=user_id)
        if name is not None:
            filters = filters & Q(name=name)
        if company is not None:
            filters = filters & Q(company=company)
        users = User.objects.filter(filters)
        return users


    def save_user(self, user: User) -> None:
        user.save()