# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import json
import gridfs

from bson.objectid import ObjectId
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from users.models import Profile
from lib.db import get_file, get_file_length, mongo_connect

db = mongo_connect()
fs = gridfs.GridFS(db)

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
        get_latest_by = "created_at"

    def is_owner(self, user):
        """Checks if an user is the owner of this object.
        @param user: user instance
        @return: boolean permission
        """
        return user == self.owner

    def is_in_users(self, user):
        """Checks if an user is allowed list of users for this object.
        @param user: user instance
        @return: boolean permission
        """
        return user in self.users

    def can_read(self, user):
        """Checks if an user is allowed to read this object.
        @param user: user instance
        @return: boolean permission
        """
        return user.is_superuser or self.is_in_users(user) or self.is_owner(user)

    def can_write(self, user):
        """Checks if an user is allowed to write (create, edit, delete) this object.
        @param user: user instance
        @return: boolean permission
        """
        return user.is_superuser or self.is_owner(user)

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
        ("P", "Processing"),
        ("Q", "Queued"),
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
        get_latest_by = "created_at"

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

    @property
    def get_file_data(self):
        """Returns image file binary data."""
        try:
            return get_file(self.image_id).read()
        except gridfs.errors.NoFile:
            raise Exception("Image not found on GridFS storage")

    @property
    def get_file_length(self):
        """Return image file size."""
        try:
            return get_file_length(self.image_id)
        except gridfs.errors.NoFile:
            raise Exception("Image not found on GridFS storage")

    @property
    def to_json(self):
        """Converts object to JSON."""
        # Fetch report from mongo.
        data = self.report
        # Cleanup.
        del(data["_id"])
        # If result available converts it.
        if data:
            return json.dumps(data, sort_keys=False, indent=4)
        else:
            return json.dumps({})

    def is_owner(self, user):
        """Checks if an user is the owner of this object.
        @param user: user instance
        @return: boolean permission
        """
        return user == self.owner

    def can_read(self, user):
        """Checks if an user is allowed to read this object.
        @param user: user instance
        @return: boolean permission
        """
        return user.is_superuser or self.is_owner(user)

    def can_write(self, user):
        """Checks if an user is allowed to write (create, edit, delete) this object.
        @param user: user instance
        @return: boolean permission
        """
        return user.is_superuser or self.is_owner(user)

@receiver(pre_delete, sender=Analysis)
def delete_mongo_analysis(sender, instance, **kwargs):
    """Hook to delete mongo data if an analysis is deleted."""

    def delete_file(uuid):
        """Deletes a file from GridFS.
        @param uuid: file UUID
        """
        try:
            obj_id = db.fs.files.find_one({"uuid": uuid})["_id"]
            fs.delete(ObjectId(obj_id))
        except:
            # TODO: add logging.
            pass

    # Fetch analysis.
    analysis = db.analyses.find_one({"_id": ObjectId(instance.analysis_id)})

    # Delete files created during analysis.
    useless_files = []

    # If analysis data are available, delete them.
    if analysis:
        # Delete ELA image.
        if "ela" in analysis and "ela_image" in analysis["ela"]:
            if db.analyses.find({"ela.ela_image": analysis["ela"]["ela_image"]}).count() == 1:
                useless_files.append(analysis["ela"]["ela_image"])
        # Delete preview images.
        if "metadata" in analysis and "preview" in analysis["metadata"]:
            for preview in analysis["metadata"]["preview"]:
                if db.analyses.find({"metadata.preview.file": preview["file"]}).count() == 1:
                    useless_files.append(preview["file"])
        # Delete analysis data.
        try:
            db.analyses.remove({"_id": ObjectId(instance.analysis_id)})
        except:
            # TODO: add logging.
            pass

    # Delete thumbnail.
    if instance.thumb_id and Analysis.objects.filter(thumb_id=instance.thumb_id).count() == 1:
        useless_files.append(instance.thumb_id)
    # Delete original image if isn't used by other analyses.
    if Analysis.objects.filter(image_id=instance.image_id).count() == 1:
        useless_files.append(instance.image_id)
    # Delete all the shit.
    for file in useless_files:
        delete_file(file)

class AnalysisMetadataDescription(models.Model):
    """Descriptors for metadata keys."""

    key = models.CharField(max_length=255, editable=False, null=False, blank=False, db_index=True, unique=True)
    description = models.TextField(editable=False, null=False, blank=False)


class Favorite(models.Model):
    """Add favorite to image."""

    analysis = models.ForeignKey(Analysis, null=False, blank=False, on_delete=models.CASCADE, db_index=True, editable=False, related_name="favorites")
    owner = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE, db_index=True, editable=False, related_name="owned_favorites")

class Comment(models.Model):
    """Add comments to image."""

    analysis = models.ForeignKey(Analysis, null=False, blank=False, on_delete=models.CASCADE, db_index=True, editable=False, related_name="comments")
    owner = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE, db_index=True, editable=False, related_name="owned_comments")
    message = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)

class Tag(models.Model):
    """Add tags to image."""

    analysis = models.ManyToManyField(Analysis)
    owner = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE, db_index=True, editable=False, related_name="owned_tags")
    text = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)