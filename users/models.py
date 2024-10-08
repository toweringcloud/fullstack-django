from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    name = models.CharField(
        max_length=150,
        blank=True,
    )
    avatar = models.CharField(
        max_length=150,
        blank=True,
    )

    def __str__(self):
        return self.username
