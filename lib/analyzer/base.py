# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from lib.utils import AutoVivification

class BaseAnalyzerModule(object):

    # Module execution order.
    order = 0

    def __init__(self):
        # Results storage.
        self.results = AutoVivification()
        # Data (results) in the global dictionary (produced by other modules).
        self.data = None

    def check_deps(self):
        raise NotImplementedError

    def run(self, task):
        raise NotImplementedError

class BaseSignature(object):
    pk = 0
    severity = 0
    category = None
    name = None
    description = None

    def check(self, data):
        raise NotImplementedError