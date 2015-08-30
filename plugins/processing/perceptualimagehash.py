# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from lib.analyzer.base import BaseProcessingModule

from lib.utils import str2image

try:
    import imagehash
    IS_IMAGEHASH = True
except ImportError:
    IS_IMAGEHASH = False


class PerceptualImageHashProcessing(BaseProcessingModule):
    """Perceptual Image Hashing."""

    name = "ImageHash Calculator"
    description = "This plugins calculates image hash using Perceptual Image Hashing."
    order = 10

    def check_deps(self):
        return IS_IMAGEHASH

    def run(self, task):
        image = str2image(task.get_file_data)

        self.results["imghash"]["a_hash"] = str(imagehash.average_hash(image))
        self.results["imghash"]["p_hash"] = str(imagehash.phash(image))
        self.results["imghash"]["d_hash"] = str(imagehash.dhash(image))

        return self.results
