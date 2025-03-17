import random
from django.core.management.base import BaseCommand
from apps.users.models import User
from apps.entrycode.models import EntryCode

def generate_unique_code():
    while True:
        code = str(random.randint(10000000, 99999999))
        if not EntryCode.objects.filter(code=code).exists():
            return code

class Command(BaseCommand):
    help = "creates entry codes if user doesnt have it"

    def handle(self, *args, **kwargs):
        users_without_codes = User.objects.filter(entry_code__isnull=True)
        
        if not users_without_codes.exists():
            self.stdout.write(self.style.SUCCESS("all users have the entry code"))
            return

        for user in users_without_codes:
            code = generate_unique_code()
            EntryCode.objects.create(user=user, code=code)
            self.stdout.write(self.style.SUCCESS(f"Created entry code: {code} for {user.fname} {user.lname} (ID: {user.user_id})"))

        self.stdout.write(self.style.SUCCESS("Done"))
