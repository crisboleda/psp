
# Django


# Django REST Framework
from rest_framework.permissions import BasePermission


class IsUserOwnerProgram(BasePermission):

    def has_object_permission(self, request, view, obj):

        if obj.program.programmer == request.user:
            return True
        return False