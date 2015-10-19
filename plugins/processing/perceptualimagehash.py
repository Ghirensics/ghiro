# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from analyses.models import Case
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

    def get_similar_images(self, hash_value, hash_func):
        # TODO: this should be refactored in the future.

        # Map.
        if hash_func == imagehash.average_hash:
            hash_name = "a_hash"
        elif hash_func == imagehash.phash:
            hash_name = "p_hash"
        elif hash_func == imagehash.dhash:
            hash_name = "d_hash"

        # Search.
        image_hash = imagehash.hex_to_hash(hash_value)
        similarities = list()
        for img in self.task.case.images.filter(state="C").exclude(id=self.task.id):
            if img.report and \
            "imghash" in img.report and \
            hash_name in img.report["imghash"] and \
            image_hash == imagehash.hex_to_hash(img.report["imghash"][hash_name]):
                # TODO: store also image distance.
                similarities.append(img.id)
        return similarities


    def run(self, task):
        self.task = task
        image = str2image(task.get_file_data)

        # Calculate hash.
        self.results["imghash"]["a_hash"] = str(imagehash.average_hash(image))
        self.results["imghash"]["p_hash"] = str(imagehash.phash(image))
        self.results["imghash"]["d_hash"] = str(imagehash.dhash(image))

        # Get similar images.
        self.results["similar"]["a_hash"] = self.get_similar_images(self.results["imghash"]["a_hash"], imagehash.average_hash)
        self.results["similar"]["p_hash"] = self.get_similar_images(self.results["imghash"]["p_hash"], imagehash.phash)
        self.results["similar"]["d_hash"] = self.get_similar_images(self.results["imghash"]["d_hash"], imagehash.dhash)

        return self.results
