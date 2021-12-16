from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from algorithms.validators import ValidateName
from .managers import CustomUserManager

from datetime import datetime, timedelta
from enum import Enum

import jwt


class ModelConsts:

    BAD_NAME = "Only letters and hyphens!"

    WORD_VALIDATOR = ValidateName(1, 2, BAD_NAME)

    EXPIRE_ACCESS = 300
    EXPIRE_REFRESH = 600


class Roles(Enum):
    """
    Enum class for different roles
    """
    admin = 0
    staff = 1
    user = 2

    @classmethod
    def items(cls):
        """ Return a tuple of choices for django.model field """
        return [(option.value, option.name) for option in cls]


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom model for user
    """
    role = models.IntegerField(choices=Roles.items(),
                               default=2)

    email = models.EmailField('email address', unique=True)

    first_name = models.CharField(max_length=128, validators=[ModelConsts.WORD_VALIDATOR, ])
    last_name = models.CharField(max_length=128, validators=[ModelConsts.WORD_VALIDATOR, ])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    objects = CustomUserManager()

    # properties
    @property
    def is_staff(self):
        return self.role < 2

    @property
    def is_admin(self):
        return self.role < 1

    @property
    def token(self):
        """ Generate new token basing on current datetime """
        return self._generate_jwt_token("access", ModelConsts.EXPIRE_ACCESS)

    @property
    def refresh_token(self):
        """ Generate new token for refreshing old tokens """
        return self._generate_jwt_token("refresh", ModelConsts.EXPIRE_REFRESH)

    def _generate_jwt_token(self, token_type: str, expire: int):
        """ Private method for generating jwt-token """
        dt = datetime.now() + timedelta(seconds=expire)

        token = jwt.encode({
            'token_type': token_type,
            'id': self.pk,
            'exp': dt.timestamp()
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


class BlacklistedToken(models.Model):
    """
    One-field model for blacklisted tokens
    """
    token = models.CharField(max_length=255, unique=True)
