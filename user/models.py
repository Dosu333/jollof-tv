from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from datetime import datetime, timezone
import uuid

TOKEN_TYPE = (
    ('PASSWORD_RESET', 'PASSWORD_RESET'),
)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(
        max_length=255, unique=True, blank=True, null=True)
    password = models.CharField(max_length=225, null=True)
    first_name = models.CharField(max_length=225, blank=True, null=True)
    last_name = models.CharField(max_length=225, blank=True, null=True)
    phone = models.CharField(max_length=17, blank=True, null=True)
    country = models.CharField(max_length=225, blank=True, null=True)
    state = models.CharField(max_length=225, blank=True, null=True)
    city = models.CharField(max_length=225, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ('-date_joined',)

    def __str__(self):
        return self.email

    def save_last_login(self):
        self.last_login = datetime.now()
        self.save()


class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    token = models.CharField(max_length=255, null=True)
    token_type = models.CharField(
        max_length=100, choices=TOKEN_TYPE, default='PASSWORD_RESET')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.user)} {self.token}"

    def is_valid(self):
        lifespan_in_seconds = float(settings.TOKEN_LIFESPAN * 60 * 60)
        now = datetime.now(timezone.utc)
        time_diff = now - self.created_at
        time_diff = time_diff.total_seconds()
        if time_diff >= lifespan_in_seconds:
            return False
        return True

    def verify_user(self):
        self.user.verified = True
        self.user.save()

    def generate(self):
        if not self.token:
            self.token = get_random_string(120)
            self.save()

    def reset_user_password(self, password):
        self.user.set_password(password)
        self.user.save()