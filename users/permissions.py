from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    The custom permission which allows only the owners of the object to edit it.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj == request.user
