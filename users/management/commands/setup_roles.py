from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, ContentType, Permission
from django.apps import apps


GROUP_PERMISSIONS = {
    'Super Admin': ['add', 'change', 'delete', 'view'],
    'Tenant Admin': ['add', 'change', 'delete', 'view'],
    'Tenant Manager': ['view', 'change'],
    'User': ['view', 'add']
}

TENANT_APPS = ['users', 'conferences', 'tenants']


class Command(BaseCommand):
    help = 'Set up default groups and assign permissions dynamically'

    def handle(self, *args, **options):
        for group_name, perms in GROUP_PERMISSIONS.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f"✅ Created group: {group_name}")

            # Get all models from tenant apps
            for app in TENANT_APPS:
                try:
                    app_config = apps.get_app_config(app)

                    for model in app_config.get_models():
                        for perm in perms:
                            codename = f"{perm}_{model._meta.model_name}"
                            try:
                                permission = Permission.objects.get(
                                    content_type__app_label=app,
                                    codename=codename
                                )
                                group.permissions.add(permission)
                            except Permission.DoesNotExist:
                                self.stdout.write(
                                    self.style.WARNING(
                                        f"⚠️ Permission {codename} not found (maybe not migrated?)"
                                    )
                                )
                except LookupError:
                    self.stdout.write(
                        self.style.WARNING(f"App {app} not found")
                    )

        self.stdout.write(self.style.SUCCESS("🎉 Successfully set up dynamic roles and permissions"))