from django.urls import path

from library.views import (
    ListBookView,
    BorrowBookView,
    StudentBorrowListView,
    RenewBookView,
    ReturnBooksView, StudentListView
)

app_name = "library"
urlpatterns = [
    path("books", ListBookView.as_view()),
    path("borrow", BorrowBookView.as_view()),
    path("student/borrow-list", StudentBorrowListView.as_view()),
    path("renew", RenewBookView.as_view()),
    path("return", ReturnBooksView.as_view()),
    path("student-list", StudentListView.as_view())
]
