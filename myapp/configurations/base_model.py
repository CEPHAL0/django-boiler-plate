from django.db.models import Model, DateTimeField
from django.utils import timezone

class BaseModel(Model):
    created_at = DateTimeField(db_index=True, default=timezone.now)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True