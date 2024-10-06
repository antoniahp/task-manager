import uuid
from django.db import models

from task_manager.domain.company.company import Company


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()
    company = models.ForeignKey(Company, related_name="projects", on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
