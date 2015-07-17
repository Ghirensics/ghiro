# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from lib.analyzer.base import BaseAnalyzerModule

try:
    import hashlib
    import zlib
    IS_HASH = True
except ImportError:
    IS_HASH = False


class HashAnalyzer(BaseAnalyzerModule):
    """Calculates some hashes."""

    order = 10

    def check_deps(self):
        return IS_HASH

    def run(self, task):
        self.results["hash"]["md5"] = hashlib.md5(task.get_file_data).hexdigest()
        self.results["hash"]['sha1'] = hashlib.sha1(task.get_file_data).hexdigest()
        self.results["hash"]["sha224"] = hashlib.sha224(task.get_file_data).hexdigest()
        self.results["hash"]["sha256"] = hashlib.sha256(task.get_file_data).hexdigest()
        self.results["hash"]["sha384"] = hashlib.sha384(task.get_file_data).hexdigest()
        self.results["hash"]["sha512"] = hashlib.sha512(task.get_file_data).hexdigest()
        self.results["hash"]["crc32"] = "%08X".lower() % (zlib.crc32(task.get_file_data) & 0xFFFFFFFF,)

        return self.results
