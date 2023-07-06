from rest_framework.permissions import BasePermission

class AdminOrTrustedUserOnly(BasePermission):
    
    def has_permission(self, request, view):
        return bool((request.user.is_superadmin or request.user.is_trusted) and request.user.is_authenticated)
    

