# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from django.core.management.base import NoArgsCommand

from ghiro.common import check_version


class Command(NoArgsCommand):
    """Checks for new Ghiro releases."""

    help = "Checks for new Ghiro releases"

    option_list = NoArgsCommand.option_list

    def handle(self, *args, **options):
        """Runs command."""

        print "Starting update check..."

        try:
            new_release = check_version()
        except Exception as e:
            print "Error occurred: %s" % e
        else:
            if new_release:
                print "New release available!"
            else:
                print "No new releases available."