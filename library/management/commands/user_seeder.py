
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from datetime import datetime


class Command(BaseCommand):
    help = 'seed fresh data users'

    def handle(self, *args, **options):
        users = [
            User(
                username="librarian",
                email="librarian@mail.com",
                password=make_password("librarian"),
                first_name="main",
                last_name="librarian",
                is_staff=True,
                date_joined=datetime.now()
            ),
            User(
                username="student",
                email="student@mail.com",
                password=make_password("student"),
                first_name="first",
                last_name="student",
                is_staff=False,
                date_joined=datetime.now()
            ),
        ]

        User.objects.bulk_create(users)
