# Ghiro - Copyright (C) 2013-2016 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from lib.analyzer.base import BaseProcessingModule


class InfoProcessing(BaseProcessingModule):
    """Collect basic information."""

    name = "Image Information"
    description = "This plugin collects basic information about the image."
    order = 10

    def check_deps(self):
        return True

    def run(self, task):
        # File name.
        self.results["file_name"] = task.file_name
        # File size
        self.results["file_size"] = task.get_file_length

        return self.results
