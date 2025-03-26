"""
Views for the venue APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Venue
from venue import serializers


class VenueViewSet(viewsets.ModelViewSet):
    """View for manage venue APIs."""
    serializer_class = serializers.VenueDetailSerializer
    queryset = Venue.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve venues for primary contact."""
        if self.request.user.is_staff or self.request.user.is_superuser:
            return self.queryset.order_by('-id')
        return self.queryset.filter(primary_contact=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        """Create a new venue."""
        if not self.request.user.is_staff:
            serializer.save(primary_contact=self.request.user)
        else:
            serializer.save()

    def create(self, request, *args, **kwargs):
        print("POST request received")
        return super().create(request, *args, **kwargs)

    def perform_update(self, serializer):
        """Create a new venue."""
        if not self.request.user.is_staff or not self.request.user.is_superuser:
            serializer.validated_data.pop('primary_contact', None)

        serializer.save()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.VenueSerializer
        return self.serializer_class
