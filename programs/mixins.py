
# Django REST Framework
from rest_framework.permissions import BasePermission


class IsOwnerProgram(BasePermission):

    def has_object_permission(self, request, view, obj):

        if obj.program.programmer != request.user:
            return False
        return True

