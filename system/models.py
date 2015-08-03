# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from datetime import datetime, timedelta
from django.db import models

class UpdateCheck(models.Model):
    """Collection of image analysis."""

    # Update check state.
    STATUSES = (
        ("E", "Error"),
        ("R", "Running"),
        ("A", "Available"),
        ("N", "Not available")
        )
    state = models.CharField(max_length=1, choices=STATUSES, default="R", editable=False, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)

    @staticmethod
    def should_check():
        """Check if application needs to check for new releases."""
        # Test each day.
        if UpdateCheck.objects.filter(created_at__gte=datetime.now()-timedelta(days=1)).order_by("-created_at").count():
            return False
        else:
            return True