# yourapp/management/commands/hash_passwords.py

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Hash passwords using Django make_password function'

    def add_arguments(self, parser):
        parser.add_argument('passwords', nargs='+', type=str, help='Passwords to hash')

    def handle(self, *args, **options):
        for password in options['passwords']:
            hashed_password = make_password(password)
            self.stdout.write(self.style.SUCCESS(f'Hashed password for "{password}": {hashed_password}'))
