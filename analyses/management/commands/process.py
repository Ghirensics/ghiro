# Ghiro - Copyright (C) 2013-2014 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import logging
from django.core.management.base import NoArgsCommand

from lib.utils import init_logging
from lib.analyzer.processing import AnalysisManager

logger = logging.getLogger(__name__)

class Command(NoArgsCommand):
    """Process images on analysis queue."""

    help = "Image processing"

    option_list = NoArgsCommand.option_list

    def handle(self, *args, **options):
        """Runs command."""
        logger.debug("Starting processor...")

        try:
            AnalysisManager().run()
        except KeyboardInterrupt:
            print "Exiting... (requested by user)"
