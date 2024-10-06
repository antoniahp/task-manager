from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from uuid import UUID

from typing_extensions import Optional

from task_manager.domain.user_story.user_story import UserStory


class UserStoryRepository(ABC):
    @abstractmethod
    def filter_user_story_by_id(self, user_story_id: UUID) -> Optional[UserStory]:
        pass
    @abstractmethod
    def filter_user_story(self, company_id: Optional[UUID] = None, user_story_id: Optional[UUID] = None, title:Optional[str] = None, estimation: Optional[int] = None, completed: Optional[bool] = None,
                     project_id: Optional[UUID] = None, assigned_user_id: Optional[UUID] = None, status_column_id: Optional[UUID] = None, completed_at:Optional[datetime] = None,
                    completed_at__gte:Optional[datetime] = None ,completed_at__lte:Optional[datetime] = None) -> List[UserStory]:
        pass

    @abstractmethod
    def save_user_story(self, user_story: UserStory) -> None:
        pass
