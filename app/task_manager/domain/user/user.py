import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from task_manager.domain.company.company import Company


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=256)
    #company = models.ForeignKey(Company, related_name="users", on_delete=models.CASCADE )

    created_at = models.DateTimeField(auto_now_add=True)

