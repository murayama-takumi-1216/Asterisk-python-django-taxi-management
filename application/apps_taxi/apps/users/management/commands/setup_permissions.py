"""
Management command to set up user groups/permissions for the taxi application.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from apps.common.constants import (
    ROL_ADMINISTRADOR,
    ROL_ADMINOPERADOR,
    ROL_ADMINTAXI,
    ROL_OPERADOR,
    ROL_ROOT,
    ROL_TAXISTA,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Set up user groups and assign permissions"

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            type=str,
            help="Username to assign administrator role",
            default="murayama",
        )
        parser.add_argument(
            "--role",
            type=str,
            help="Role to assign (administrador, operador, etc.)",
            default="administrador",
        )

    def handle(self, *args, **options):
        username = options["username"]
        role = options["role"]

        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(
            self.style.SUCCESS("Setting up Groups and Permissions")
        )
        self.stdout.write(self.style.SUCCESS("=" * 60))

        # Define all roles
        roles = [
            ROL_ROOT,
            ROL_ADMINISTRADOR,
            ROL_ADMINOPERADOR,
            ROL_ADMINTAXI,
            ROL_OPERADOR,
            ROL_TAXISTA,
        ]

        # Create groups
        self.stdout.write("\n1. Creating groups...")
        for role_name in roles:
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"   ✓ Created group: {role_name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"   - Group already exists: {role_name}")
                )

        # Assign role to user
        self.stdout.write(f"\n2. Assigning role to user '{username}'...")
        try:
            user = User.objects.get(username=username)

            # Get the group
            group = Group.objects.get(name=role)

            # Clear existing groups (optional)
            # user.groups.clear()

            # Add the new group
            user.groups.add(group)

            self.stdout.write(
                self.style.SUCCESS(
                    f"   ✓ Assigned '{role}' role to user '{username}'"
                )
            )

            # Display user's current groups
            user_groups = list(user.groups.values_list("name", flat=True))
            self.stdout.write(
                self.style.SUCCESS(
                    f"   Current groups for '{username}': {', '.join(user_groups)}"
                )
            )

        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f"   ✗ User '{username}' does not exist!"
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    f"   Create the user first or use --username=<existing_user>"
                )
            )
        except Group.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"   ✗ Role '{role}' does not exist!")
            )
            self.stdout.write(
                self.style.WARNING(
                    f"   Available roles: {', '.join(roles)}"
                )
            )

        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("✓ Setup Complete!"))
        self.stdout.write("=" * 60)
        self.stdout.write("\nNext steps:")
        self.stdout.write("1. Logout from the application")
        self.stdout.write(f"2. Login as '{username}'")
        self.stdout.write("3. You should now see the dashboard and menu items!\n")
