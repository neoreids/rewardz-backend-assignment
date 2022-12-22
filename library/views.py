from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


# Create your views here.
from library.models import Books, BorrowedBooks
from library.filters import ListBookFilter
from library.serializers import PublicListBookSerializer, BorrowBookSerializerPost, ResponseBorrowedSerializer, \
    UserListSerializers
from library.request_object.borrow_request import BorrowRequest
from library.logic.borrow import BorrowLogics
from library.permissions import IsStudent, IsLibrarian


class ListBookView(ListCreateAPIView):
    permission_classes = []
    queryset = Books.objects.all()
    serializer_class = PublicListBookSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ListBookFilter


class BorrowBookView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsLibrarian]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BorrowBookSerializerPost
        return ResponseBorrowedSerializer

    def post(self, request):
        payload = request.data
        user_id = payload.get("user_id")
        books = payload.get("books")

        request_object = BorrowRequest(user_id=user_id, books=books)
        logics = BorrowLogics.borrow(request_object)

        return Response(logics)


class StudentBorrowListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    queryset = BorrowedBooks.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user_id=request.user.id).order_by("-id").all()
        serializer = ResponseBorrowedSerializer(queryset, many=True)
        return Response(serializer.data)


class RenewBookView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsLibrarian]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BorrowBookSerializerPost
        return ResponseBorrowedSerializer

    def post(self, request):
        payload = request.data
        user_id = payload.get("user_id")
        books = payload.get("books")

        request_object = BorrowRequest(user_id=user_id, books=books)
        logics = BorrowLogics.renew(request_object)

        return Response(logics)


class ReturnBooksView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsLibrarian]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BorrowBookSerializerPost
        return ResponseBorrowedSerializer

    def post(self, request):
        payload = request.data
        user_id = payload.get("user_id")
        books = payload.get("books")

        request_object = BorrowRequest(user_id=user_id, books=books)
        logics = BorrowLogics.return_book(request_object)

        return Response(logics)


class StudentListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsLibrarian]
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(is_staff=False).order_by("-id")
        serializer = UserListSerializers(queryset, many=True)
        return Response(serializer.data)
