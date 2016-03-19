# Ghiro - Copyright (C) 2013-2016 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import os
import sys
from django.core.management.base import BaseCommand
from optparse import make_option

from analyses.models import Case, Analysis
from users.models import Profile
from lib.exceptions import GhiroValidationException


class Command(BaseCommand):
    """Image submission via command line."""

    option_list = BaseCommand.option_list + (
        make_option("--target", "-t", dest="target",
            help="Path of the file or directory to submit"),
        make_option("--case", "-c", dest="case",
            help="Case ID, images will be attached to it"),
        make_option("--username", "-u", dest="username",
            help="Username"),
        make_option("--recurse", "-r", dest="recurse", default=False,
            action="store_true", help="Recurse inside subdirectories"),
    )

    help = "Task submission"

    def handle(self, *args, **options):
        """Runs command."""
        # Validation.
        if not options["username"] or not options["case"] or not options["target"]:
            print("Options -t (target), -c (case id) and -u (username) are mandatory. Exiting.")
            sys.exit(1)

        # Get options.
        user = Profile.objects.get(username=options["username"].strip())
        case = Case.objects.get(pk=options["case"].strip())

        # Add directory or files.
        if os.path.isdir(options["target"]) and options["recurse"]:
            for dirname, dirnames, filenames in os.walk(options["target"]):
                for filename in filenames:
                    target = os.path.join(dirname, filename)
                    print("INFO: adding {0}".format(target))
                    self._add_task(target, case, user)
        elif os.path.isdir(options["target"]):
            for file_name in os.listdir(options["target"]):
                print("INFO: adding {0}".format(file_name))
                self._add_task(os.path.join(options["target"], file_name), case, user)
        elif os.path.isfile(options["target"]):
            print("INFO: processing {0}".format(options["target"]))
            self._add_task(options["target"], case, user)
        else:
            print("ERROR: target is not a file or directory")

    def _add_task(self, target, case, user):
        """Wraps add_task() to catch errors."""
        try:
            Analysis.add_task(target, case=case, user=user)
        except GhiroValidationException as e:
            print("ERROR: %s" % e)