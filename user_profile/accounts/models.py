from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

from smartfields import fields
from django_countries.fields import CountryField


class UserManager(BaseUserManager):
    """Create and manage users."""
    def create_user(self, first_name, last_name, email, username=None, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        """if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")"""
        if not username:
            # username = email.split('@')[0]
            raise ValueError("Users must have a username")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name, email, password, username=None):
        user = self.create_user(
            first_name,
            last_name,
            email,
            username,
            password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User model data."""
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=40, unique=True, null=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # USERNAME_FIELD = 'email'
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['first_name', 'last_name']
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return "@{}".format(self.username)

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return "{} {} (@{})".format(self.first_name, self.last_name,
                                    self.username)


class UserProfile(models.Model):
    """User profile data."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = fields.ImageField(upload_to='avatar_photos/', blank=True, null=True)
    location = models.CharField(max_length=40, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    preferred_position = models.CharField(max_length=40, blank=True, null=True)
    preferred_foot = models.CharField(max_length=40, blank=True, null=True)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)
