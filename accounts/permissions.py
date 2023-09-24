from rest_framework import permissions
from django.contrib.auth.models import User
from .models import Organization,JobSeeker

class isOrganizationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # print(view.kwargs['username'])
        if request.method in permissions.SAFE_METHODS:
            return True
        if(not request.user.is_authenticated):
                return False
        user= User.objects.filter(email=request.user.email)
        if not user.exists():
            return False
            
        organization = Organization.objects.filter(user=user[0].id)
        if not organization.exists() :
            return False
        
        if organization[0].user.username==view.kwargs['username']:
            return True
        
        return False

    
    