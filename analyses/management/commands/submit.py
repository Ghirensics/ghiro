# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import magic
import os
import sys
from django.core.management.base import BaseCommand
from optparse import make_option

from analyses.models import Case, Analysis
from lib.db import save_file
from lib.utils import create_thumb
from users.models import Profile
from ghiro.common import check_allowed_content


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
            print "Options -t (target), -c (case id) and -u (username) are mandatory. Exiting."
            sys.exit(1)

        # Get options.
        user = Profile.objects.get(username=options["username"].strip())
        case = Case.objects.get(pk=options["case"].strip())

        # Add directory or files.
        if os.path.isdir(options["target"]) and options["recurse"]:
            for dirname, dirnames, filenames in os.walk(options["target"]):
                for filename in filenames:
                    target = os.path.join(dirname, filename)
                    print "INFO: adding {0}".format(target)
                    self._add_task(target, case, user)
        elif os.path.isdir(options["target"]):
            for file_name in os.listdir(options["target"]):
                print "INFO: adding {0}".format(file_name)
                self._add_task(os.path.join(options["target"], file_name), case, user)
        elif os.path.isfile(options["target"]):
            print "INFO: processing {0}".format(options["target"])
            self._add_task(options["target"], case, user)
        else:
            print "ERROR: target is not a file or directory"

    def _add_task(self, file, case, user):
        """Adds a new task to database.
        @param file: file path
        @param case: case id
        @param user: user id
        """
        # File type check.
        mime = magic.Magic(mime=True)
        content_type = mime.from_file(file)
        if not check_allowed_content(content_type):
            print "WARNING: Skipping %s: file type not allowed." % file
        else:
            # Add to analysis queue.
            Analysis(onwer=user, case=case, file_name=os.path.basename(file),
                    image_id=save_file(file_path=file, content_type=content_type),
                    thumb_id=create_thumb(file)).save()