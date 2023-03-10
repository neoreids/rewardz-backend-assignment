from rest_framework.serializers import ModelSerializer, SerializerMethodField, \
    Serializer, IntegerField, ListField

from library.models import Books, BorrowedBooks
from django.contrib.auth.models import User

class BookBaseSerializer(ModelSerializer):

    is_available = SerializerMethodField()
    will_be_returned_at = SerializerMethodField()

    def get_is_available(self, obj: Books):
        return obj.is_available

    def get_will_be_returned_at(self, obj: Books):
        return obj.returned_at

    class Meta:
        model = Books
        fields = "__all__"


class PublicListBookSerializer(BookBaseSerializer):
    total_stock = SerializerMethodField()

    def get_total_stock(self, obj: Books):
        return obj.total_available


class BorrowBookSerializerPost(Serializer):
    user_id = IntegerField()
    books = ListField()


class ResponseBorrowedSerializer(ModelSerializer):

    title = SerializerMethodField()
    author = SerializerMethodField()
    will_returned_at = SerializerMethodField()

    def get_title(self, obj: BorrowedBooks):
        return obj.book.title

    def get_author(self, obj: BorrowedBooks):
        return obj.book.author

    def get_will_returned_at(self, obj: BorrowedBooks):
        return obj.will_returned_at.strftime("%b %d %Y %H:%M:%S")

    class Meta:
        model = BorrowedBooks
        fields = ("user_id", "title", "author", "will_returned_at", "book_id")


class UserListSerializers(ModelSerializer):

    active_borrowed_books = SerializerMethodField()

    def get_active_borrowed_books(self, obj: User):
        queryset = obj.user_borrowed.filter(is_returned=False).order_by("-id").all()
        return ResponseBorrowedSerializer(queryset, many=True).data

    history_borrowed = SerializerMethodField()

    def get_history_borrowed(self, obj: User):
        queryset = obj.user_borrowed.order_by("-id").all()
        return ResponseBorrowedSerializer(queryset, many=True).data

    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "active_borrowed_books", "history_borrowed")