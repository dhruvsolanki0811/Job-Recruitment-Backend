from rest_framework import permissions
class isOrganizationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request)
        print(view.kwargs,'has')
        return False
    def has_object_permission(self, request, view, obj):
        print(request)
        print(view.kwargs)
        print(obj)
        
        return False