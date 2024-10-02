from django.db import models
class TaskType(models.TextChoices):
    TASK = "task"
    SUBTASK = "subtask"
    USER_HISTORY = "user_history"
