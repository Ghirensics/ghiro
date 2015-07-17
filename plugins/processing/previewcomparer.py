# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import logging
from itertools import izip

from lib.analyzer.base import BaseAnalyzerModule
from lib.utils import str2image
from lib.db import get_file

try:
    from PIL import Image
    IS_PIL = True
except ImportError:
    IS_PIL = False

logger = logging.getLogger(__name__)


class ImageComparer():
    """Image comparator."""

    @staticmethod
    def calculate_difference(preview, original_image_id):
        """Calculate difference between two images.
        @param preview: preview dict
        @param original_image_id: original image ID
        @return: difference, difference percentage
        """
        try:
            i1 = str2image(get_file(original_image_id).read())
        except IOError as e:
            logger.warning("Comparer error reading image: {0}".format(e))
            return

        # Check if thumb was resized.
        if "original_file" in preview:
            i2 = str2image(get_file(preview["original_file"]).read())
        else:
            i2 = str2image(get_file(preview["file"]).read())

        # Resize.
        width, height = i2.size
        try:
            i1 = i1.resize([width, height], Image.ANTIALIAS)
        except IOError as e:
            logger.warning("Comparer error reading image: {0}".format(e))
            return

        # Checks.
        #assert i1.mode == i2.mode, "Different kinds of images."
        #assert i1.size == i2.size, "Different sizes."

        # Calculate difference.
        pairs = izip(i1.getdata(), i2.getdata())
        if len(i1.getbands()) == 1:
            # for gray-scale jpegs
            dif = sum(abs(p1-p2) for p1,p2 in pairs)
        else:
            dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))

        ncomponents = i1.size[0] * i1.size[1] * 3

        # Get diff percentage.
        diff_perc = int((dif / 255.0 * 100) / ncomponents)

        # Binary option.
        if diff_perc >= 15:
            diff = True
        else:
            diff = False

        return diff, diff_perc


class PreviewComparerAnalyzer(BaseAnalyzerModule):
    """Compares previews extracted with the original image."""

    order = 20

    def check_deps(self):
        return IS_PIL

    def run(self, task):
        # Compare previews to catch differences.
        if "metadata" in self.results:
            if "preview" in self.results["metadata"]:
                for preview in self.results["metadata"]["preview"]:
                    difference = ImageComparer.calculate_difference(preview, self.results["file_data"])
                    if difference:
                        preview["diff"], preview["diff_percent"] = difference

        return self.results
