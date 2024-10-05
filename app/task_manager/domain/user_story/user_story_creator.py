from datetime import datetime
from typing import Optional
from uuid import UUID

from task_manager.domain.user_story.user_story import UserStory


class UserStoryCreator:
    def create_user_story(self, user_story_id: UUID, title:str, description:str, estimation: int, completed: bool, completed_at:datetime, project_id: Optional[UUID] = None,  assigned_user_id: Optional[UUID] = None, status_column_id: Optional[UUID] = None ) -> UserStory:
        return UserStory(
            id=user_story_id,
            title=title,
            description=description,
            estimation=estimation,
            completed=completed,
            project_id=project_id,
            assigned_user_id=assigned_user_id,
            status_column_id=status_column_id,
            completed_at=completed_at,
        )