# Ghiro - Copyright (C) 2013-2014 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import logging
from django.core.management.base import NoArgsCommand
from django.utils.timezone import now
from django.db import transaction
from django.db.models import Q
from time import sleep
from multiprocessing import Pool

import analyzer.db as db
from analyses.models import Analysis
from analyzer.images import AnalyzerRunner
from analyzer.utils import HashComparer

logger = logging.getLogger("processor")

class Command(NoArgsCommand):
    """Process images on analysis queue."""

    help = "Image processing"

    option_list = NoArgsCommand.option_list

    def handle(self, *args, **options):
        """Runs command."""
        logger.debug("Starting processor...")

        try:
            self._process()
        except KeyboardInterrupt:
            print "Exiting... (requested by user)"

    def _process(self):
        """Starts processing waiting tasks."""

        # Processing pool.
        pool = Pool()

        # Clean up tasks remaining stale from old runs.
        Analysis.objects.filter(Q(state="P")|Q(state="Q")).update(state="W")

        while True:
            # Clean django model cache.
            transaction.enter_transaction_management()
            transaction.commit()

            # Fetch tasks waiting processing.
            tasks = Analysis.objects.filter(state="W").order_by("id")

            if tasks.exists():
                logger.info("Found {0} images waiting".format(tasks.count()))

                for task in tasks:
                    # Mark as enqueued for processing.
                    task.state = "Q"
                    task.save()

                    # Send to processing pool.
                    pool.apply_async(_analyze, [task])

                logger.info("Done bunch")
            else:
                logger.debug("Waiting...")
                sleep(1)

def _analyze(task):
    # Mark task as processing.
    logger.info("Processing task {0}".format(task.id))
    task.state = "P"
    task.save()

    try:
        # Process.
        results = AnalyzerRunner(task.image_id, task.file_name).run()
        task.analysis_id = db.save_results(results)
        # Hash checks.
        HashComparer.run(results["hash"], task)
        # Complete.
        task.state = "C"
        logger.info("Processed task {0} with success".format(task.id))
    except Exception as e:
        logger.exception("Error processing task {0}: {1}".format(task.id, e))
        task.state = "F"
    finally:
        # Save.
        task.completed_at = now()
        task.save()