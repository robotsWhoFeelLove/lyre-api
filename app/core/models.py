"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_org = models.CharField(max_length=255)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Venue(models.Model):
    """Venue Object"""
    venue_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    primary_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    @classmethod
    def get_default_venue_pk(cls):
        """Returns or creates a default venue for the database."""
        if not cls.objects.exists():
            return None
        venue, created = cls.objects.get_or_create(
            venue_name='default venue'
        )
        return venue.pk


class Group(models.Model):
    """Returns or creates a default group for the database."""
    group_name = models.CharField(max_length=255, default="default group")
    primary_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)

    @classmethod
    def get_default_group_pk(cls):
        if not cls.objects.exists():
            return None
        group, created = cls.objects.get_or_create(
            group_name='default group'
        )
        return group.pk

    # @classmethod
    # def get_default_group_pk(cls):

    #     return cls.get_default_group().pk


class SubGroup(models.Model):
    """Returns or creates a default subgroupfor the database."""
    group_id = models.ForeignKey(
        settings.GROUP_MODEL,
        on_delete=models.CASCADE,
        null=False,
        default=Group.get_default_group_pk
    )
    display_name = models.CharField(max_length=255, null=True, blank=True)

    @classmethod
    def get_default_subgroup_pk(cls):
        if not cls.objects.exists():
            return None
        subgroup, created = cls.objects.get_or_create(
            display_name='default subgroup'
        )
        return subgroup.pk


class Event(models.Model):
    """Event object."""
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    duration = models.IntegerField(default=0)
    datetime = models.DateTimeField(null=True)
    venue_id = models.ForeignKey(
        settings.VENUE_MODEL,
        on_delete=models.CASCADE,
        null=False,
        default=Venue.get_default_venue_pk
    )
    group_id = models.ForeignKey(
        settings.GROUP_MODEL,
        on_delete=models.CASCADE,
        null=False,
        default=Group.get_default_group_pk
    )
    description = models.TextField(blank=True)
    subgroup_id = models.ForeignKey(
        settings.SUBGROUP_MODEL,
        on_delete=models.CASCADE,
        null=False,
        default=SubGroup.get_default_subgroup_pk
    )

    def __str__(self):
        return self.title
