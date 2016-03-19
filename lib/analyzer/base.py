# Ghiro - Copyright (C) 2013-2016 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from lib.utils import AutoVivification

class BaseProcessingModule(object):
    """Abstract class for processing modules.
    It provides basic methods to check dependencies, run the module and store results.
    """
    # Module execution order.
    order = 0
    # Plugin name.
    name = None
    # Plugin description.
    description = None

    def __init__(self):
        # Results storage.
        self.results = AutoVivification()
        # Data (results) in the global dictionary (produced by other modules).
        self.data = None

    def check_deps(self):
        """Checks if all the module dependencies are installed."""
        raise NotImplementedError

    def run(self, task):
        """Run the module."""
        raise NotImplementedError

class BaseSignature(object):
    pk = 0
    severity = 0
    category = None
    name = None
    description = None

    def check(self, data):
        raise NotImplementedError