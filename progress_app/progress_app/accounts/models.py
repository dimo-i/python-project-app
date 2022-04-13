from django.core.validators import MinLengthValidator
from django.db import models

from progress_app.accounts.managers import ProgressAppUserManager
from progress_app.common.validators import validate_letters

from django.contrib.auth import models as auth_models


class ProgressAppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_MIN_LENGTH = 5
    USERNAME_MAX_LENGTH = 30

    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=(
            MinLengthValidator(USERNAME_MIN_LENGTH),
        ),
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
        # editable=True,
    )


    USERNAME_FIELD = 'username'

    objects = ProgressAppUserManager()

class Profile(models.Model):
    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 25

    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 25

    GENDERS = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_letters,
        ),
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_letters,
        ),
    )

    email = models.EmailField()

    profile_picture = models.URLField()

    gender = models.CharField(
        max_length=15,
        choices=GENDERS,
        null=True,
        blank=True,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    date_created = models.DateTimeField(
        'date created',
        auto_now_add=True,
    )

    user = models.OneToOneField(
        ProgressAppUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    # TODO fix deletion(is_active not settled accordingly in user)
    def delete(self):
        self.is_active = False
        self.user.is_active=False
        self.save()