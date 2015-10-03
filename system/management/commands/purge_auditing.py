# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from django.core.management.base import NoArgsCommand

from users.models import Activity


class Command(NoArgsCommand):
    """Purge auditing table."""

    help = "Purge auditing table"

    option_list = NoArgsCommand.option_list

    def handle(self, *args, **options):
        """Runs command."""

        print "Audit log purge"
        print "WARNING: this will permanently delete all your audit logs!"
        try:
            ans = bool(input("Do you want to continue? [y/n]"))
        except NameError:
            print "Please use only y/n"
        else:
            if ans:
                print "Purging audit log... (it could take several minutes)"
                Activity.objects.all().delete()
                print "Done."