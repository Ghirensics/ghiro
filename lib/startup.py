# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import logging
import os
import shutil
from django.conf import settings

from analyses.models import Case

logger = logging.getLogger(__name__)

def create_auto_upload_dirs():
    """Creates the directory tree used in upload from file system feature.
    It creates the AUTO_UPLOAD_DIR directory and a folder for each case with the Syntax 'Case_id_1' where 1 is
    the case ID.
    Folders have the following structure:
        AUTO_UPLOAD_DIR
            |
            |--- Case_id_1
            |--- Case_id_2
            |--- etc. (one for each case)
    """
    # Sync cases if auto upload is enabled.
    if settings.AUTO_UPLOAD_DIR:
        logger.debug("Auto upload from directory is enabled on %s.", settings.AUTO_UPLOAD_DIR)

        # Cleanup auto upload directory:
        if settings.AUTO_UPLOAD_STARTUP_CLEANUP and os.path.exists(settings.AUTO_UPLOAD_DIR):
            logger.debug("Cleaning up %s.", settings.AUTO_UPLOAD_DIR)
            try:
                shutil.rmtree(settings.AUTO_UPLOAD_DIR)
            except IOError as e:
                logger.error("Unable to clean auto upload directory %s reason %s" % (settings.AUTO_UPLOAD_DIR, e))
                return False

        # Create directory if it's missing.
        if not os.path.exists(settings.AUTO_UPLOAD_DIR):
            logger.debug("Auto upload directory is missing, creating it.")
            try:
                os.mkdir(settings.AUTO_UPLOAD_DIR)
            except IOError as e:
                logger.error("Unable to create auto upload main directory %s reason %s" % (settings.AUTO_UPLOAD_DIR, e))
                return False

        # Create cases dirs.
        for case in Case.objects.all():
            dir_path = os.path.join(settings.AUTO_UPLOAD_DIR, case.directory_name)
            if not os.path.exists(dir_path):
                try:
                    logger.debug("Creating directory %s" % dir_path)
                    os.mkdir(dir_path)
                except IOError as e:
                    logger.error("Unable to create auto upload case directory %s reason %s" % (dir_path, e))
                    continue
    else:
        return False