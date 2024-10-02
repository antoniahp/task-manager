import uuid

from django.db import models

from config import settings
from task_manager.domain.project.project import Project
from task_manager.domain.sprint.sprint import Sprint
from task_manager.domain.task.task_type import TaskType
from task_manager.domain.user.user import User


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=256)
    description = models.TextField()
    punctuation = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)
    task_type = models.CharField(max_length=16,choices=TaskType.choices)
    parent_task = models.ForeignKey("task_manager.Task", related_name='parent_tasks', on_delete=models.CASCADE)
    sprint = models.ForeignKey(Sprint, related_name='sprint_tasks', on_delete=models.PROTECT)
    project = models.ForeignKey(Project, related_name='project_tasks', on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
