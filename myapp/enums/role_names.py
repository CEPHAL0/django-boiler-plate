from enum import Enum

class BaseEnum(Enum):
    def __get__(self, instance, owner):
        return self.value

    def __str__(self):
        return self.value

class RoleNameEnum(BaseEnum):
    SUPER_ADMIN = 'Super Admin'
    TENANT_ADMIN = 'Tenant Admin'