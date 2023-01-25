from rest_framework.permissions import SAFE_METHODS, BasePermission


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class UserReadOnly(BasePermission):
    def has_permission(self, request, view):
        is_authenticated = bool(request.user and request.user.is_authenticated)
        if not is_authenticated:
            return False

        if request.user.is_staff or request.method in SAFE_METHODS:
            return True

        return False


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.owner.id
