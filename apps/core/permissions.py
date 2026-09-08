from rest_framework.permissions import BasePermission 


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.author.id == user.id and user.is_verified


class IsVerified(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_verified