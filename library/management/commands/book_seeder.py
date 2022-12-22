from django.core.management.base import BaseCommand
from library.models import Books
from faker import Faker
from random import randint


class Command(BaseCommand):
    help = 'seed fresh data for books'

    def handle(self, *args, **options):
        fake = Faker()
        books = [Books(title=fake.sentence(), author=fake.name(), quantity=randint(10, 99)) for _ in range(10)]
        Books.objects.bulk_create(books)
