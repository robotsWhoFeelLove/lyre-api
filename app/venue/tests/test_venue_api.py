"""
Tests for Venue APIs
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Venue

from venue.serializers import (
    VenueSerializer,
    VenueDetailSerializer
)


VENUES_URL = reverse('venue:venue-list')


def detail_url(venue_id):
    """Vreate and return a venue detail URL."""
    return reverse('venue:venue-detail', args=[venue_id])


def create_venue(**params):
    """Create and return a sample venue."""

    user, created = get_user_model().objects.get_or_create(
        email='test@example.com',
        password='test123'
    )
    defaults = {
        'venue_name': 'Smalls',
        'address': '10339 Conant, Hamtramck, MI 48212',
        'primary_contact': user,
    }

    defaults.update(params)

    venue = Venue.objects.create(**defaults)
    return venue


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicVenueAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(VENUES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateVenueAPITests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()

        self.user = create_user(
            email='user@example.com', password='password123')
        self.client.force_authenticate(self.user)
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin1@example.com',
            password='testpass123'
        )

    def test_retrieve_venues(self):
        create_venue(primary_contact=self.user)
        create_venue(primary_contact=self.user, venue_name='Smalls2')

        res = self.client.get(VENUES_URL)

        venues = Venue.objects.all().order_by('-id')
        serializer = VenueSerializer(venues, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_venue_list_limited_to_user(self):
        """Test list of venues is limited to authenticated user."""
        other_user = create_user(
            email='other2@example.com',
            password='password123'
        )
        create_venue(primary_contact=other_user)
        create_venue(primary_contact=self.user)

        res = self.client.get(VENUES_URL)
        venues = Venue.objects.filter(primary_contact=self.user)
        serializer = VenueSerializer(venues, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_venue(self):
        """Test creating a venue."""
        payload = {
            'venue_name': 'Created Venue',
            'address': '123 Created Venue Lane',
        }

        res = self.client.post(VENUES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        venue = Venue.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(venue, k), v)
        self.assertEqual(venue.primary_contact, self.user)

    def test_venue_list_all_for_admin(self):
        """Test admin receives all venues."""
        self.client.force_authenticate(self.admin_user)
        other_user = get_user_model().objects.create_user(
            'other2@example.com',
            'password123'
        )
        create_venue(primary_contact=other_user)
        create_venue(primary_contact=self.user)

        res = self.client.get(VENUES_URL)
        venues = Venue.objects.all().order_by('-id')
        serializer = VenueSerializer(venues, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_venue_detail(self):
        """Test get venue detail."""
        venue = create_venue(primary_contact=self.user)

        url = detail_url(venue.id)
        res = self.client.get(url)

        serializer = VenueDetailSerializer(venue)
        self.assertEqual(res.data, serializer.data)

    def test_partial_update(self):
        """Test partial update of venue"""
        original_address = "123 Original Lane"
        venue = create_venue(
            primary_contact=self.user,
            venue_name='Original Venue Name',
            address=original_address
        )

        payload = {
            'venue_name': 'Changed Venue Name'
        }

        url = detail_url(venue.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        venue.refresh_from_db()
        self.assertEqual(venue.venue_name, payload['venue_name'])
        self.assertEqual(venue.address, original_address)
        self.assertEqual(venue.primary_contact, self.user)

    def test_full_update(self):
        """Test full update of venue"""

        venue = create_venue(
            primary_contact=self.user,
            venue_name='Original Venue Name',
            address='123 Original Lane'
        )

        other_user = create_user(
            email='someOtherUser@example.com',
            password='123NewPassword'
        )

        payload = {
            'venue_name': 'Changed Venue Name',
            'address': "123 Brand New Avenue",
            'primary_contact': other_user.id
        }

        self.client.force_authenticate(self.admin_user)

        url = detail_url(venue.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        venue.refresh_from_db()
        self.assertEqual(venue.venue_name, payload['venue_name'])
        self.assertEqual(venue.address, payload['address'])
        self.assertEqual(venue.primary_contact, other_user)

    def test_non_admin_update_contact_fails(self):
        """Test partial update of venue"""
        venue = create_venue(
            primary_contact=self.user,
            venue_name='Original Venue Name',
            address="123 Original Lane"
        )

        other_user = create_user(
            email='someOtherUser2@example.com',
            password='123NewPassword'
        )

        payload = {
            'primary_contact': other_user.id
        }

        self.client.force_authenticate(self.user)

        url = detail_url(venue.id)
        res = self.client.patch(url, payload)

        venue.refresh_from_db()
        self.assertEqual(venue.primary_contact, self.user)

    def test_delete_venue(self):
        """Test deleting a venue is successful."""
        venue = create_venue(primary_contact=self.user)

        url = detail_url(venue.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Venue.objects.filter(id=venue.id).exists())

    def test_delete_other_users_venue(self):
        """Test deleting another users venue gives an error."""
        venue = create_venue(primary_contact=self.user)
        other_user = create_user(
            email='someOtherUser@test.com', password="test123pass")

        self.client.force_authenticate(other_user)
        url = detail_url(venue.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Venue.objects.filter(id=venue.id).exists())
