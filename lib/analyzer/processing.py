# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import logging
import pkgutil
import inspect

from time import sleep
from multiprocessing import cpu_count, Process, JoinableQueue
from django.utils.timezone import now
from django.conf import settings

import plugins.processing as modules
from lib.utils import AutoVivification
from analyses.models import Analysis
from lib.analyzer.base import BaseProcessingModule
from lib.db import save_results

logger = logging.getLogger(__name__)


class AnalysisRunner(Process):
    """Run an analysis process."""

    def __init__(self, tasks, modules=None):
        Process.__init__(self)
        self.tasks = tasks
        self.modules = modules
        logger.debug("AnalysisRunner started")

    def run(self):
        """Start processing."""
        # Antani-finite loop.
        while True:
            try:
                # Get a new task from queue.
                task = self.tasks.get()
                self._process_image(task)
            except KeyboardInterrupt:
                break

    def _process_image(self, task):
        """Process an image.
        @param task: image task
        """
        try:
            results = {}

            # Save reference to image data on  GridFS.
            results["file_data"] = task.image_id

            for module in self.modules:
                current = module()
                current.data = results
                try:
                    output = current.run(task)
                except Exception as e:
                    logger.exception("Critical error in plugin {0}, skipping: {1}".format(module, e))
                    continue
                else:
                    if isinstance(output, AutoVivification):
                        results.update(output)
                    else:
                        logger.warning("Module %s returned results not in dict format." % module)

            # Complete.
            task.analysis_id = save_results(results)
            task.state = "C"
            logger.info("Processed task {0} with success".format(task.id))
        except Exception as e:
            logger.exception("Critical error processing task {0}, skipping task: {1}".format(task.id, e))
            task.state = "F"
        finally:
            # Save.
            task.completed_at = now()
            task.save()
            self.tasks.task_done()


class AnalysisManager():
    """Manage all analysis' process."""

    def __init__(self):
        # Processing pool.
        logger.debug("Using pool on %i core" % self.get_parallelism())
        # Load modules.
        self.modules = []
        self.load_modules()
        self.check_module_deps()
        # Starting worker pool.
        self.workers = []
        self.tasks = JoinableQueue(self.get_parallelism())
        self.workers_start()

    def workers_start(self):
        """Start workers pool."""
        for _ in range(self.get_parallelism()):
            runner = AnalysisRunner(self.tasks, self.modules)
            runner.start()
            self.workers.append(runner)

    def workers_stop(self):
        """Stop workers pool."""
        # Wait for.
        for sex_worker in self.workers:
            sex_worker.join()

    def get_parallelism(self):
        """Get the ghiro parallelism level for analysis processing."""
        # Check database type. If we detect SQLite we slow down processing to
        # only one process. SQLite does not support parallelism.
        if settings.DATABASES["default"]["ENGINE"].endswith("sqlite3"):
            logger.warning("Detected SQLite database, decreased parallelism to 1. SQLite doesn't support parallelism.")
            return 1
        elif cpu_count() > 1:
            # Set it to total CPU minus one let or db and other use.
            return cpu_count() - 1
        else:
            return 1

    def load_modules(self):
        """Load modules."""
        # Search for analysis modules, it need to import module directory as package named "modules".
        for loader_instance, module_name, is_pkg in pkgutil.iter_modules(modules.__path__, modules.__name__ + "."):
            # Skip packages.
            if is_pkg:
                continue
            # Load module.
            # NOTE: This code is inspired to Cuckoo Sandbox module loading system.
            try:
                module = __import__(module_name, globals(), locals(), ["dummy"], -1)
            except ImportError as e:
                logger.error("Unable to import module: %s" % module)
            else:
                for class_name, class_pkg in inspect.getmembers(module):
                    if inspect.isclass(class_pkg):
                        # Load only modules which inherits BaseModule.
                        if issubclass(class_pkg, BaseProcessingModule) and class_pkg is not BaseProcessingModule:
                            self.modules.append(class_pkg)
                            logger.debug("Found module: %s" % class_name)

        # Sort modules by execution order.
        self.modules.sort(key=lambda x: x.order)

    def check_module_deps(self):
        """Check modules for requested deps, if not found removes the module from the list."""
        for plugin in self.modules:
            # NOTE: create the module class instance.
            if not plugin().check_deps():
                self.modules.remove(plugin)
                logger.warning("Kicked module, requirements not found: %s" % plugin.__name__)

    def run(self):
        """Start all analyses."""
        # Clean up tasks remaining stale from old runs.
        if Analysis.objects.filter(state="P").exists():
            logger.info("Found %i stale analysis, putting them in queue." % Analysis.objects.filter(state="P").count())
            Analysis.objects.filter(state="P").update(state="W")

        # Infinite finite loop.
        try:
            while True:
                # Fetch tasks waiting processing.
                tasks = Analysis.objects.filter(state="W").order_by("id")

                if tasks.exists() and not self.tasks.full():
                    # Using iterator() to avoid caching.
                    for task in Analysis.objects.filter(state="W").order_by("id").iterator():
                        self.tasks.put(task)
                        logger.debug("Processing task %s" % task.id)
                        task.state = "P"
                        task.save()
                elif self.tasks.full():
                    logger.debug("Queue full. Waiting...")
                    sleep(1)
                else:
                    logger.debug("No tasks. Waiting...")
                    sleep(1)
        except KeyboardInterrupt:
            print("Exiting... (requested by user)")
        finally:
            print("Waiting tasks to accomplish...")
            self.workers_stop()
            print("Processing done. Have a nice day in the real world.")
