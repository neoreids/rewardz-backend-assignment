from rest_framework.exceptions import APIException
from rest_framework import status


class MaxBorrowedReach(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        "message": "this user have reach maximum limit to borrow books"
    }


class BookOutOfStock(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        "message": "all book already borrowed"
    }


class BookAlreadyBorrowed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        "message": "book Already Borrowed, Return it first or you can renew once"
    }


class BookAlreadyRenewed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        "message": "book is already renewed"
    }


class RenewDisallowed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        "message": "can't renew, the period has been reached"
    }