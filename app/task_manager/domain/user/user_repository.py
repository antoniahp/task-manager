from abc import abstractmethod, ABC
from typing import Optional
from uuid import UUID

from task_manager.domain.user.user import User


class UserRepository(ABC):
    @abstractmethod
    def filter_user_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    def filter_users(self, user_id: Optional[UUID], name: Optional[str], company:Optional[UUID]) -> Optional[User]:
        pass

    @abstractmethod
    def save_user(self, user: User) -> None:
        pass