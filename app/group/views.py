"""
Views for the group APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
)

from core.models import Group
from group import serializers


class GroupViewSet(viewsets.ModelViewSet):
    """View for manage group APIs."""
    serializer_class = serializers.GroupSerializer
    queryset = Group.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """Retrieve groups for admin contact."""
        return self.queryset.order_by('-id')

    def perform_create(self, serializer):
        """Create a new group."""
        serializer.save()

    def create(self, request, *args, **kwargs):
        print("POST request received")
        return super().create(request, *args, **kwargs)

    # def perform_update(self, serializer):
    #     """Create a new venue."""
    #     if not self.request.user.is_staff or not self.request.user.is_superuser:
    #         serializer.validated_data.pop('primary_contact', None)

    #     serializer.save()

    # def get_serializer_class(self):
    #     """Return the serializer class for request."""
    #     if self.action == 'list':
    #         return serializers.VenueSerializer
    #     return self.serializer_class
