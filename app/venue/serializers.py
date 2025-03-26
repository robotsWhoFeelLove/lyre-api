"""
serializers for venue APIs
"""
from rest_framework import serializers

from core.models import Venue


class VenueSerializer(serializers.ModelSerializer):
    """Serializer for venues"""

    class Meta:
        model = Venue
        fields = ['id', 'venue_name', 'address']
        read_only_fields = ['id']


class VenueDetailSerializer(serializers.ModelSerializer):
    """Serializer for venue detail"""

    class Meta(VenueSerializer.Meta):
        fields = VenueSerializer.Meta.fields + ['primary_contact']
