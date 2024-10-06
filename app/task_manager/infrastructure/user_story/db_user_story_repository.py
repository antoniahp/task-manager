from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from uuid import UUID

from django.db.models import Q
from typing_extensions import Optional

from task_manager.domain.user_story.user_story import UserStory
from task_manager.domain.user_story.user_story_repository import UserStoryRepository


class DbUserStoryRepository(UserStoryRepository):
    def filter_user_story_by_id(self, user_story_id: UUID) -> Optional[UserStory]:
        user_story = UserStory.objects.filter(id=user_story_id).first()
        return user_story
    def filter_user_story(self, user_story_id: Optional[UUID] = None, title:Optional[str] = None, estimation: Optional[int] = None, completed: Optional[bool] = None,
                     project_id: Optional[UUID] = None, assigned_user_id: Optional[UUID] = None, status_column_id: Optional[UUID] = None, completed_at:Optional[datetime] = None,
                    completed_at__gte:Optional[datetime] = None ,completed_at__lte:Optional[datetime] = None, company_id: Optional[UUID] = None,) -> List[UserStory]:
        filters = Q()
        if user_story_id is not None:
            filters = filters & Q(id=user_story_id)
        if company_id is not None:
            filters = filters & Q(project__company_id=company_id)
        if title is not None:
            filters = filters & Q(title=title)
        if estimation is not None:
            filters = filters & Q(estimation=estimation)
        if completed is not None:
            filters = filters & Q(completed=completed)
        if project_id is not None:
            filters = filters & Q(project_id=project_id)
        if assigned_user_id is not None:
            filters = filters & Q(assigned_user_id=assigned_user_id)
        if status_column_id is not None:
            filters = filters & Q(status_column_id=status_column_id)
        if completed_at is not None:
            filters = filters & Q(completed_at=completed_at)
        if completed_at__gte is not None:
            filters = filters & Q(completed_at__gte=completed_at__gte)
        if completed_at__lte is not None:
            filters = filters & Q(completed_at__lte=completed_at__lte)

        user_stories = UserStory.objects.filter(filters)
        return user_stories

    def save_user_story(self, user_story: UserStory) -> None:
        user_story.save()
