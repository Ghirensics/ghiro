# Ghiro - Copyright (C) 2013-2016 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import logging

from lib.analyzer.base import BaseProcessingModule
from lib.utils import str2image

try:
    from nude import Nude
    IS_NUDEPY = True
except ImportError:
    IS_NUDEPY = False

logger = logging.getLogger(__name__)

class NudePyProcessing(BaseProcessingModule):
    """Detects nude using NudePy."""

    name = "Nude Detection (NudePy)"
    description = "This plugins detects images of nude using NudePy."
    order = 10

    def check_deps(self):
        return IS_NUDEPY

    def run(self, task):
        try:
            tmp_image = str2image(task.get_file_data)
            n = Nude(tmp_image)
            # The resize is used to have although less accurate processing.
            # TODO: move this to options panel.
            n.resize(maxwidth=1000)
            n.parse()
        except Exception as e:
            logger.warning("[Task {0}]: Error detecting nude: {1}".format(task.id, e))
        else:
            self.results["nude"]["nudepy"]["result"] = n.result
            self.results["nude"]["nudepy"]["msg"] = n.message

        return self.results
