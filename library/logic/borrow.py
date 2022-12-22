from datetime import datetime
from dateutil.relativedelta import relativedelta

from library.exceptions import MaxBorrowedReach, BookOutOfStock, BookAlreadyBorrowed, BookAlreadyRenewed, \
    RenewDisallowed
from library.request_object.borrow_request import BorrowRequest
from library.models import BorrowedBooks, Books
from library.serializers import ResponseBorrowedSerializer
from rewardz.constants import MAX_BORROW


class BorrowLogics:

    @staticmethod
    def borrow(req: BorrowRequest):
        total_borrow = BorrowedBooks.objects.count_borrowed_by_student(req.user_id)
        if total_borrow >= MAX_BORROW:
            raise MaxBorrowedReach()

        will_returned_at = datetime.now() + relativedelta(months=+1)
        list_borrowed = []

        for i in req.books:
            book = Books.objects.filter(id=i).first()

            if not book.is_available:
                raise BookOutOfStock()

            already_borrowed = BorrowedBooks.objects.filter(
                book_id=i,
                user_id=req.user_id, is_returned=False
            ).exists()

            if already_borrowed:
                raise BookAlreadyBorrowed()

            borrowed = BorrowedBooks(
                book=book,
                user_id=req.user_id,
                will_returned_at=will_returned_at
            )
            list_borrowed.append(borrowed)

        create_borrowed = BorrowedBooks.objects.bulk_create(list_borrowed)
        response = ResponseBorrowedSerializer(create_borrowed, many=True)
        return response.data

    def get_borrowed_by_user_and_books(self, user_id: int, books: [int]):
        books = BorrowedBooks.objects.filter(user_id=user_id, book_id__in=books, is_returned=False).all()
        return books

    @staticmethod
    def renew(req: BorrowRequest):
        today = datetime.now()
        books = BorrowLogics().get_borrowed_by_user_and_books(req.user_id, req.books)

        for book in books:
            if book.is_renewed:
                raise BookAlreadyRenewed()

            if not today.date() <= book.will_returned_at.date():
                raise RenewDisallowed()

            return_deadline = today + relativedelta(months=+1)
            book.will_returned_at = return_deadline
            book.is_renewed = True
            book.save()

        response = ResponseBorrowedSerializer(books, many=True)
        return response.data

    @staticmethod
    def return_book(req: BorrowRequest):
        books = BorrowedBooks.objects.filter(user_id=req.user_id, book_id__in=req.books, is_returned=False).all()

        for book in books:
            book.is_returned = True
            book.save()

        response = ResponseBorrowedSerializer(books, many=True)
        return response.data