from rest_framework import permissions


class IsLibrarian(permissions.BasePermission):
    message = "only librarian can access this side"

    def has_permission(self, request, view):
        return request.user.is_staff


class IsStudent(permissions.BasePermission):
    message = "only student can access this side"

    def has_permission(self, request, view):
        return not request.user.is_staff