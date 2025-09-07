from django.db import models
from django.contrib.auth.models import AbstractUser
from myapp.configurations.base_model import BaseModel

# Create your models here.
class User(AbstractUser, BaseModel):
    class Meta:
        db_table = 'users'

    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email or self.username