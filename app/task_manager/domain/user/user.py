import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import UUID
from task_manager.domain.company.company import Company


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=256)
    company = models.ManyToManyField(Company, related_name="users")

    created_at = models.DateTimeField(auto_now_add=True)

    def belongs_to_company(self, company_id: UUID) -> bool:
        return self.company.filter(id=company_id).exists()



