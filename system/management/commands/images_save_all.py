import os
import sys

from django.core.management.base import NoArgsCommand
from bson.objectid import InvalidId
from optparse import make_option

from analyses.models import Analysis
from lib.db import get_file


class Command(NoArgsCommand):

    help = "Save all images to a directory"

    option_list = NoArgsCommand.option_list + (
        make_option("-p", "--path", action="store", type="str", dest="path"),
    )

    def handle(self, *args, **options):
        print "Starting"

        if os.path.exists(options["path"]):
            dst_path = os.path.join(options["path"], "ghiro_output")
            if os.path.exists(dst_path):
                print "ERROR: a folder 'ghiro_output' already exist in that path!"
                sys.exit()
            else:
                # Create destination folder.
                os.mkdir(dst_path)

                # We are fine, run!
                for analysis in Analysis.objects.all():
                    try:
                       file = get_file(analysis.image_id)
                    except (InvalidId, TypeError) as e:
                        print "Unable to dump %s: %s" % (analysis.id, e)
                        continue
                    else:
                        with open(os.path.join(dst_path, "analysis_%s" % analysis.id), "a") as the_file:
                            the_file.write(file.read())
        else:
            print "ERROR: path not found!"