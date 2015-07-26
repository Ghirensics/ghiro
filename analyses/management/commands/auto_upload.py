# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import os
import re
import logging
import sys
from time import sleep
from django.conf import settings
from django.core.management.base import NoArgsCommand

from analyses.models import Analysis, Case

logger = logging.getLogger(__name__)

class Command(NoArgsCommand):
    """Monitor a directory for new files."""

    help = "Directory monitor and images upload."

    option_list = NoArgsCommand.option_list

    def handle(self, *args, **options):
        """Runs command."""
        logger.debug("Starting directory monitoring...")

        # Path.
        monitor_path = settings.AUTO_UPLOAD_DIR
        # Preventive check.
        if not monitor_path:
            logger.error("Missing AUTO_UPLOAD_DIR in your configuration file, aborting.")
            sys.exit()

        logger.info("Monitoring directory %s" % monitor_path)

        try:
            self.run(monitor_path)
        except KeyboardInterrupt:
            print "Exiting... (requested by user)"

    def submit_file(self, path, case):
        """Submit a file for analysis.
        @param path: file path
        @param case: case instance
        """
        # Submit.
        Analysis.add_task(path, case=case, user=case.owner)
        # Delete original file:
        if settings.AUTO_UPLOAD_DEL_ORIGINAL:
            os.remove(path)

    def parse_dir_name(self, path):
        """Parses case directory name.
        @param path: directory path.
        @return: case instance
        """
        case_match = re.search("Case_id_([\d]+)$", path)
        case_id = case_match.group(1)
        case = Case.objects.get(pk=case_id)
        return case

    def run(self, path):
        """Starts directory monitoring for new images.
        @param path: auto upload directory path"""
        # List of already scanned files.
        files_found = []

        # Antani loop.
        while True:
            for dir_name, dir_names, file_names in os.walk(path):
                for file_name in file_names:
                    target = os.path.join(dir_name, file_name)
                    # Check if already scanned.
                    if not target in files_found:
                        logger.debug("Found new file %s" % target)

                        # Parse case ID from directory name.
                        case = self.parse_dir_name(target)
                        if case:
                            # Submit image.
                            self.submit_file(target, case)

            # Check for removed files.
            for file in files_found:
                if not os.path.exists(file):
                    files_found.remove(file)

            # Wait for next cycle.
            sleep(30)