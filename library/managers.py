from django.db.models import Manager


class BorrowedBooksManager(Manager):
    def count_borrowed(self, book_id):
        return self.filter(book_id=book_id, is_returned=False).count()

    def count_borrowed_by_student(self, student_id):
        return self.filter(is_returned=False, user_id=student_id).count()

