from types import SimpleNamespace

class PermissionEnumMeta(type):
    """
    Metaclass to dynamically generate CRUD permissions for any model accessed.
    Example: PermissionEnum.Conference.add => "add_conference"
    """
    def __getattr__(cls, model_name):
        # Normalize to lowercase for codename convention
        model_name_lower = model_name.lower()
        # Return a SimpleNamespace with standard CRUD permissions
        return SimpleNamespace(
            add=f"add_{model_name_lower}",
            change=f"change_{model_name_lower}",
            delete=f"delete_{model_name_lower}",
            view=f"view_{model_name_lower}"
        )

class PermissionEnum(metaclass=PermissionEnumMeta):
    pass