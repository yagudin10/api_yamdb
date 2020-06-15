from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user



class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            if request.user.is_staff:
                return True


class IsAdmin(BasePermission):
    allowed_user_roles = ('admin', )

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role in self.allowed_user_roles:
                return True
        return False

class IsOwnerOrStaffOrReadOnly(BasePermission):
    allowed_user_roles = ('admin', 'moderator', )
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.user.role in self.allowed_user_roles:
                return True
            return obj.author == request.user
        return False
