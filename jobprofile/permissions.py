from rest_framework import permissions
from django.contrib.auth.models import User
from accounts.models import Organization
import json

class isOrganizationPermissionOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # print(view.kwargs['username'])
        if request.method in permissions.SAFE_METHODS:
            return True
        if(not request.user.is_authenticated):
                return False
        user= User.objects.filter(email=request.user.email)
        if not user.exists():
            return False
        reqbody=json.loads(request.body.decode('utf-8'))

        organization = Organization.objects.filter(user=user[0].id,id=reqbody['organization_id'])
        
        if not organization.exists() :
            return False
        
        
        return True

    
    