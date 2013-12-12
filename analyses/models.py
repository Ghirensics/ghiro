# Ghiro - Copyright (C) 2013 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.


from bson.objectid import ObjectId
from django.db import models
from django.conf import settings

from ghiro.common import mongo_connect
from users.models import Profile

db = mongo_connect()

class Case(models.Model):
    """Collection of image analysis."""

    # Case state.
    STATUSES = (
        ("O", "Open"),
        ("C", "Closed")
    )
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=1, choices=STATUSES, default="O", db_index=True, editable=False, null=False, blank=False)
    owner = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE, db_index=True, editable=False, related_name="owned_cases")
    users = models.ManyToManyField(Profile, null=True, blank=True, db_index=True, related_name="cases")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        if self.description:
            self.description = self.description.strip()
        super(Case, self).save(*args, **kwargs)

class Analysis(models.Model):
    """Image analysis."""

    STATUSES = (
        ("W", "Waiting"),
        ("C", "Completed"),
        ("F", "Failed")
    )
    image_id = models.CharField(max_length=72, editable=False, null=False, blank=False)
    thumb_id = models.CharField(max_length=72, editable=False, null=True, blank=True)
    file_name = models.CharField(max_length=255, editable=False, null=False, blank=False)
    analysis_id = models.CharField(max_length=24, db_index=True, editable=False, null=True, blank=True)
    case = models.ForeignKey(Case, null=False, blank=False, on_delete=models.CASCADE, db_index=True, editable=False, related_name="images")
    owner = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE, db_index=True, editable=False, related_name="owned_images")
    state = models.CharField(max_length=1, choices=STATUSES, default="W", db_index=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def latitude(self):
        """Lookups latitude on mongo."""
        try:
            record = db.analyses.find_one({"_id": ObjectId(self.analysis_id)})
        except:
            return None

        if "gps" in record["metadata"]:
            return record["metadata"]["gps"]["pos"]["Latitude"]

    @property
    def longitude(self):
        """Lookups longitude on mongo."""
        try:
            record = db.analyses.find_one({"_id": ObjectId(self.analysis_id)})
        except:
            return None

        if "gps" in record["metadata"]:
            return record["metadata"]["gps"]["pos"]["Longitude"]

    @property
    def report(self):
        """Lookups report on mongo, used to fetch anal."""
        try:
            return db.analyses.find_one(ObjectId(self.analysis_id))
        except:
            return None

class AnalysisMetadataDescription(models.Model):
    """Descriptors for metadata keys."""

    key = models.CharField(max_length=255, editable=False, null=False, blank=False, db_index=True, unique=True)
    description = models.TextField(editable=False, null=False, blank=False)


class Favorite(models.Model):
    """Add favorite to image."""

    analysis = models.ForeignKey(Analysis, null=False, blank=False, on_delete=models.CASCADE, db_index=True, editable=False, related_name="favorites")
    owner = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE, db_index=True, editable=False, related_name="owned_favorites")
