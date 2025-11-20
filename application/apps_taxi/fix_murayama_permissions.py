#!/usr/bin/env python
"""
Quick script to fix murayama user permissions.
Run this from the apps_taxi directory.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
os.environ.setdefault('DJANGO_READ_DOT_ENV_FILE', 'True')

# Setup Django path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Initialize Django
django.setup()

# Now import Django models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

def main():
    print("=" * 60)
    print("Fixing murayama user permissions")
    print("=" * 60)

    # 1. Get or create all groups
    print("\n1. Creating groups...")
    groups_to_create = [
        'root',
        'administrador',
        'adminoperador',
        'admintaxi',
        'operador',
        'taxista',
    ]

    for group_name in groups_to_create:
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"   [OK] Created group: {group_name}")
        else:
            print(f"   [EXISTS] Group exists: {group_name}")

    # 2. Fix murayama user
    print("\n2. Updating murayama user...")
    try:
        user = User.objects.get(username='murayama')

        # Make user staff (required for Django admin access)
        user.is_staff = True
        user.is_superuser = True  # Give superuser access
        user.save()

        print(f"   [OK] Set is_staff = True")
        print(f"   [OK] Set is_superuser = True")

        # Assign administrador group
        admin_group = Group.objects.get(name='administrador')
        user.groups.add(admin_group)

        print(f"   [OK] Added to 'administrador' group")

        # Show current groups
        user_groups = list(user.groups.values_list('name', flat=True))
        print(f"\n   Current groups: {', '.join(user_groups)}")

    except User.DoesNotExist:
        print(f"   [ERROR] User 'murayama' not found!")
        return

    print("\n" + "=" * 60)
    print("[SUCCESS] murayama is now ready!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Go to: http://localhost:8000/admin/")
    print("2. Login as: murayama")
    print("3. You should now have full admin access!")
    print("\nOr for the main application:")
    print("1. Logout and login again as murayama")
    print("2. You should see the full dashboard and menu\n")

if __name__ == '__main__':
    main()
