# Ghiro - Copyright (C) 2013-2016 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import codecs
import json
import os
from django.conf import settings
from lib.analyzer.base import BaseProcessingModule


class JsonExport(BaseProcessingModule):
    """JSON Export."""

    name = "JSON Export"
    description = "This plugins exports the analysis data in JSON format."
    order = 90 # Last plugin set.

    def check_deps(self):
        return True

    def run(self, task):
        indent = 4
        encoding = "utf-8"

        # Skip if plugin is diabled.
        if not settings.JSON_EXPORT:
            return self.results

        # Create reports directory.
        path = os.path.join(settings.PROJECT_DIR, "reports")
        if not os.path.exists(path):
            os.mkdir(path)

        file_path = os.path.join(path, "Analysis %i.json" % task.id)

        with codecs.open(file_path, "w", "utf-8") as report:
            json.dump(self.data, report, sort_keys=False,
                      indent=int(indent), encoding=encoding)

        return self.results
