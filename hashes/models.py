# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from django.db import models

from analyses.models import Profile, Analysis

class List(models.Model):
    """Hashes list."""
    CIPHERS = (
            ("sha1", "SHA1"),
            ("sha224", "SHA224"),
            ("sha384", "SHA384"),
            ("crc32", "CRC32"),
            ("sha256", "SHA256"),
            ("sha512", "SHA512"),
            ("md5", "MD5")
            )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    cipher = models.CharField(max_length=6, choices=CIPHERS, db_index=True, null=False, blank=False, default="MD5")
    public = models.BooleanField(default=False)
    owner = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE, db_index=True, editable=False, related_name="owned_hashes")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    matches = models.ManyToManyField(Analysis, null=True, blank=True)

class Hash(models.Model):
    """Hashes."""
    value = models.CharField(max_length=255)
    list = models.ForeignKey(List, null=False, blank=False, on_delete=models.CASCADE, db_index=True, editable=False)