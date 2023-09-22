# permissions.py
# from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsProjectAuthor(BasePermission):
    """
    Custom permission to allow only the project's author to modify or delete it.
    """
    def has_object_permission(self, request, _, obj):
       
        return obj.author == request.user


class IsContributorOrProjectAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        
        if obj.author == request.user:
            return True
        
        if obj.contributor_set.filter(user=request.user).exists():
            return True
        return False

