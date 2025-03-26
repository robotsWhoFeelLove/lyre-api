"""
Tests for models.
"""
# from decimal import Decimal
from datetime import datetime
import pytz

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_Successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # def test_create_event(self):
    #     """Test creating an event is successful."""
    #     user = get_user_model().objects.create_user(
    #         'test@example.com',
    #         'test123'
    #     )
    #     group = get_user_model().objects.create
    #     event = models.Event.objects.create(
    #         last_modified_by=user,
    #         title='Sample event',
    #         duration=45,
    #         datetime=pytz.timezone(
    #             'US/Eastern').localize(datetime.datetime(2025, 3, 21, 10, 30)),
    #         venue_id="001",
    #         group_id='Blowout 2025',
    #         description='Test band description.',
    #         subgroup='Friday'
    #     )

        # self.assertEqual(str(event), event.title)
