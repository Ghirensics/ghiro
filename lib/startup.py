# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import logging
import os
from django.conf import settings

from analyses.models import Case

logger = logging.getLogger(__name__)

def create_auto_upload_dirs():
    """Creates the directory tree used in upload from file system feature."""
    # Sync cases if auto upload is enabled.
    if settings.AUTO_UPLOAD_DIR:
        logger.debug("Auto upload from directory is enabled.")
        # Create the directory if it doesn't exist.
        if not os.path.exists(settings.AUTO_UPLOAD_DIR):
            try:
                os.mkdir(settings.AUTO_UPLOAD_DIR)
            except IOError as e:
                logger.error("Unable to create auto upload main directory %s reason %s" % (settings.AUTO_UPLOAD_DIR, e))

        # Create cases dirs.
        for case in Case.objects.all():
            dir_name = "Case_id_%s" % case.id
            dir_path = os.path.join(settings.AUTO_UPLOAD_DIR, dir_name)
            if not os.path.exists(dir_path):
                try:
                    logger.debug("Creating directory %s" % dir_path)
                    os.mkdir(dir_path)
                except IOError as e:
                    logger.error("Unable to create auto upload case directory %s reason %s" % (dir_path, e))