import uuid

from django.db import models

from config import settings
from task_manager.domain.project.project import Project
from task_manager.domain.sprint.sprint import Sprint
from task_manager.domain.task.task_type import TaskType


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=256)
    description = models.TextField()
    estimation = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)
    category = models.CharField(max_length=16,choices=TaskType.choices)
    parent_task = models.ForeignKey("task_manager.Task", related_name='subtasks', on_delete=models.PROTECT)
    sprint = models.ForeignKey(Sprint, related_name='tasks', on_delete=models.PROTECT)
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
