from rest_framework.permissions import BasePermission
from .models import Company


class IsAdminUser(BasePermission):
    
    #Allows access only to users whose company role is ADMIN.

    def has_permission(self, request, view):

        # User must be authenticated
        if not request.user.is_authenticated:
            return False

        # User must have a Company profile
        if not hasattr(request.user, "company"):
            return False

        # Check if the company role is ADMIN
        return request.user.company.role == Company.Role.ADMIN