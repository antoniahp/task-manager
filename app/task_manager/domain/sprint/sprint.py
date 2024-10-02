import uuid
from django.db import models

class Sprint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=256)
    objective = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
