from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password=None, **extra_fields):

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):

        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    bio = models.CharField(max_length=300, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    confirmation_code = models.TextField(max_length=32, blank=True)
    email_confirmed = models.BooleanField(default=False)

    objects = UserManager()

    class Role(models.TextChoices):
        user = 'user'
        moderator = 'moderator'
        admin = 'admin'

    role = models.CharField(
        max_length=9,
        blank=True,
        choices=Role.choices,
        default=Role.user,
    )
