# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from lib.analyzer.base import BaseAnalyzerModule

try:
    import magic
    IS_MAGIC = True
except ImportError:
    IS_MAGIC = False


class MimeAnalyzer(BaseAnalyzerModule):
    """Extracts MIME information."""

    order = 10

    def check_deps(self):
        return IS_MAGIC

    def get_magic_filetype(self, file_data):
        """Get magic file type.
        @param file_data: file data
        @return: file type
        """
        mime = magic.Magic(mime=True)
        return mime.from_buffer(file_data)

    def get_filetype(self, file_data):
        """Get extended file type.
        @param file_data: file data
        @return: file type
        """
        return magic.from_buffer(file_data)

    def run(self, task):
        # Get simple MIME type, example: 'image/png'
        self.results["mime_type"] = self.get_magic_filetype(task.get_file_data)
        # Get extended file type, example: 'PNG image data, 651 x 147, 8-bit/color RGB, non-interlaced'
        self.results["file_type"] = self.get_filetype(task.get_file_data)

        return self.results
