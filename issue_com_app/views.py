from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import IssueSerializers, CommentSerializer
from .models import Issue, Comment
from proj_contrib_app.models import Contributor, Project
from django.db.models import Q
from softdesk.permissions import IsIssueAuthorOrAdmin




class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializers
    permission_classes = [permissions.IsAuthenticated, IsIssueAuthorOrAdmin]
    
    def get_queryset(self):
        user = self.request.user
        # Retrieves the issues where the user is either a project contributor or the assigned contributor
        return Issue.objects.filter(Q(project__contributor__user=user) | Q(assigned_contributor__user=user))


    def create(self, request, *args, **kwargs):
        project = Project.objects.get(pk=request.data['project'])

        # If the user is not already a contributor, add them as a contributor.
        if not project.contributor_set.filter(user=request.user).exists():
            Contributor.objects.create(user=request.user, project=project)

        # Create a mutable copy of request.data.
        data = request.data.copy()

        # Update 'author' with the ID of the logged-in user
        data['author'] = request.user.id

        # Use this modified copy for the serializer.
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Save the object with the updated author.
        issue = serializer.save(author=request.user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

def perform_create(self, serializer):
    serializer.save(author=self.request.user)




class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only contributors of the project associated with the issue can view the comments.
        user = self.request.user
        return Comment.objects.filter(issue__project__contributor__user=user)

    def create(self, request, *args, **kwargs):
        issue = Issue.objects.get(pk=request.data['issue'])
        
        # Check if the user is either the author of the issue, 
        # a contributor to the project associated with the issue, or the user assigned to this issue.
        
        if not (issue.author == request.user or issue.project.contributor_set.filter(user=request.user).exists() or issue.assigned_contributor.user == request.user):
            return Response({"detail": "Vous n'avez pas le droit de commenter cette issue."}, status=status.HTTP_403_FORBIDDEN)

        # Manually add the author of the comment.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
