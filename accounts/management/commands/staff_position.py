from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from app.models import StaffPosition

class Command(BaseCommand):
    help = 'Create predefined staff positions and assign permissions'

    def handle(self, *args, **kwargs):
        # Create Staff Positions
        self.create_staff_positions()

        # Assign permissions to each position
        self.assign_permissions()

    def create_staff_positions(self):
        """
        Create predefined staff positions if they don't already exist.
        """
        positions = [
            ('Doctor', 'Can manage patients, consultations, manage patient records, and appointments'),
            ('Receptionist', 'Can schedule appointments, manage patient records'),
            ('Nurse/Medical Assistant', 'Can assist doctors, manage inventory'),
            ('IT Staff', 'Can manage the website and user accounts'),
            ('Administrator', 'Can create other staff accounts but isn’t a superuser'),
        ]
        
        for title, description in positions:
            if not StaffPosition.objects.filter(title=title).exists():
                StaffPosition.objects.create(title=title, description=description)
                self.stdout.write(self.style.SUCCESS(f'Created staff position: {title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Staff position already exists: {title}'))

    def assign_permissions(self):
        """
        Assign permissions to each staff position.
        """
        # Permissions for each role
        role_permissions = {
            'Doctor': ['can_manage_patients', 'can_schedule_appointments', 'can_manage_patient_records', 'can_manage_consultations'],
            'Receptionist': ['can_schedule_appointments', 'can_manage_patient_records'],
            'Nurse/Medical Assistant': ['can_assist_doctors', 'can_manage_inventory'],
            'IT Staff': ['can_manage_patients', 'can_schedule_appointments', 'can_manage_patient_records', 'can_manage_consultations', 'can_manage_users', 'can_manage_website', 'can_create_staff_accounts'],
            'Administrator': ['can_manage_patients', 'can_schedule_appointments', 'can_manage_patient_records', 'can_manage_consultations', 'can_manage_users', 'can_manage_website', 'can_create_staff_accounts'],
        }

        for position, permissions in role_permissions.items():
            staff_position = StaffPosition.objects.get(title=position)
            
            # Ensure the Group associated with the StaffPosition exists
            group = staff_position.group
            if group:
                for perm_codename in permissions:
                    try:
                        permission = Permission.objects.get(codename=perm_codename)
                        group.permissions.add(permission)
                        self.stdout.write(self.style.SUCCESS(f'Assigned permission "{perm_codename}" to {position}'))
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'Permission "{perm_codename}" does not exist.'))
