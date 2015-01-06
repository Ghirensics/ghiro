# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(AbstractUser):
    """User profile."""

    api_key = models.CharField(default=uuid4, max_length=36, null=False, blank=False, unique=True, db_index=True)

class Activity(models.Model):
    """Audits users activities."""

    CATEGORIES = (
        ("A", "Admin"),
        ("I", "Analysis"),
        ("H", "Hash List"),
        ("C", "Case")
        )
    message = models.TextField(null=False, blank=False)
    category = models.CharField(max_length=1, choices=CATEGORIES, db_index=True, editable=False, null=False, blank=False)
    user = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE, db_index=True, editable=False)
    source_ip = models.GenericIPAddressField(null=False, blank=False)
    forwarded_for_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)

    class Meta:
        ordering = ["-created_at"]