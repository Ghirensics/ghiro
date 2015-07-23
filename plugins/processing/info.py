# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from lib.analyzer.base import BaseAnalyzerModule


class InfoAnalyzer(BaseAnalyzerModule):
    """Collect basic information."""

    order = 10

    def check_deps(self):
        return True

    def run(self, task):
        # File name.
        self.results["file_name"] = task.file_name
        # File size
        self.results["file_size"] = task.get_file_length

        return self.results
