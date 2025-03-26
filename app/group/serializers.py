"""
serializers for group APIs
"""
from rest_framework import serializers

from core.models import Group


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for groups"""

    class Meta:
        model = Group
        fields = ['id', 'group_name', 'primary_contact']
        read_only_fields = ['id']


# class VenueDetailSerializer(serializers.ModelSerializer):
#     """Serializer for venue detail"""

#     class Meta(VenueSerializer.Meta):
#         fields = VenueSerializer.Meta.fields + ['primary_contact']
