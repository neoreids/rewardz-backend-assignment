from django.db import models
from django.contrib.auth.models import User


# schema of book
from library.managers import BorrowedBooksManager


class Books(models.Model):
    title = models.CharField(max_length=255, null=False)
    quantity = models.IntegerField(null=False, default=10)
    author = models.CharField(max_length=255, null=False, default="default author")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def total_available(self):
        borrowed = BorrowedBooks.objects.count_borrowed(self.id)
        return self.quantity - borrowed

    @property
    def is_available(self):
        available = self.total_available
        return available > 0

    @property
    def returned_at(self):
        if self.is_available:
            return None

        borrowed = BorrowedBooks.objects.filter(book=self).order_by("-will_returned_at").first()
        return borrowed.will_returned_at.strftime("%b %d %Y %H:%M:%S")


class BorrowedBooks(models.Model):
    book = models.ForeignKey(Books, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="user_borrowed")
    is_renewed = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)
    will_returned_at = models.DateTimeField(null=False)
    created_at = models.DateTimeField(auto_now=True)

    objects = BorrowedBooksManager()

