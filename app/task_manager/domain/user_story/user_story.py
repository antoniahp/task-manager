import uuid

from django.db import models

from config import settings
from task_manager.domain.project.project import Project
from task_manager.domain.status_column.status_column import StatusColumn

class UserStory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=256)
    description = models.TextField()
    estimation = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    status_column = models.ForeignKey(StatusColumn, related_name='user_stories', on_delete=models.PROTECT, null=True, blank=True)
    project = models.ForeignKey(Project, related_name='user_stories', on_delete=models.PROTECT, null=True, blank=True)
    assigned_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)