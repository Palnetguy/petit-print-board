"""
Django management command to create sample users for testing

Usage:
    python manage.py create_sample_users
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create sample users for testing (1 secretary, 3 teachers)'

    def handle(self, *args, **options):
        # Create secretary
        if not User.objects.filter(username='secretary').exists():
            secretary = User.objects.create_user(
                username='secretary',
                password='secretary123',
                email='secretary@kabgayi.edu',
                first_name='Marie',
                last_name='Mukamana',
                is_staff=True,
                is_superuser=False
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Created secretary: secretary / secretary123'))
        else:
            self.stdout.write(self.style.WARNING('- Secretary account already exists'))

        # Create sample teachers
        teachers = [
            {'username': 'teacher1', 'first_name': 'Jean', 'last_name': 'Baptiste', 'email': 'jean@kabgayi.edu'},
            {'username': 'teacher2', 'first_name': 'Alice', 'last_name': 'Uwamahoro', 'email': 'alice@kabgayi.edu'},
            {'username': 'teacher3', 'first_name': 'Patrick', 'last_name': 'Niyonzima', 'email': 'patrick@kabgayi.edu'},
        ]

        for teacher_data in teachers:
            if not User.objects.filter(username=teacher_data['username']).exists():
                User.objects.create_user(
                    username=teacher_data['username'],
                    password='teacher123',
                    email=teacher_data['email'],
                    first_name=teacher_data['first_name'],
                    last_name=teacher_data['last_name'],
                    is_staff=False,
                    is_superuser=False
                )
                self.stdout.write(self.style.SUCCESS(
                    f'✓ Created teacher: {teacher_data["username"]} / teacher123'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'- Teacher {teacher_data["username"]} already exists'
                ))

        self.stdout.write(self.style.SUCCESS('\n✅ Sample users created successfully!'))
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  Secretary: secretary / secretary123')
        self.stdout.write('  Teachers:  teacher1, teacher2, teacher3 / teacher123')
