import uuid

from django.db import models

from task_manager.domain.company.company import Company


class StatusColumn(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=64)
    company = models.ForeignKey(Company, related_name='status_column', on_delete=models.PROTECT)
    order = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)