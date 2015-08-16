# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import tempfile
import os
import logging

from lib.analyzer.base import BaseProcessingModule
from lib.db import save_file
from lib.utils import image2str, str2temp_file

try:
    from PIL import Image, ImageChops, ImageEnhance, ImageFile
    IS_PIL = True
except ImportError:
    IS_PIL = False

logger = logging.getLogger(__name__)


class ElaProcessing(BaseProcessingModule):
    """Calculates ELA."""

    name = "ELA Analysis"
    description = "This plugin performs Error Level Analysis (ELA)."
    order = 20

    def check_deps(self):
        return IS_PIL

    def run(self, task):
        # NOTE: used to allow processing of malformed images.
        # With default settings they raise errors like "IOError: image file is truncated (0 bytes not processed)".
        # See: http://stackoverflow.com/questions/9211719/python-pil-image-error-after-image-load
        ImageFile.LOAD_TRUNCATED_IMAGES = True

        # Check this kind of analysis should be run on this file type.
        # It can be applied only on PNG and JPEG formats.
        if "mime_type" in self.data and not (self.data["mime_type"] == "image/png" or self.data["mime_type"] == "image/jpeg"):
            return False

        # Create temporary file.
        handle, resaved = tempfile.mkstemp()
        tmp_file = str2temp_file(task.get_file_data)
        # Open file and resave it.
        try:
            im = Image.open(tmp_file.name)
            im.save(resaved, "JPEG", quality=95)
            resaved_im = Image.open(resaved)
        except IOError as e:
            logger.warning("ELA error opening image: {0}".format(e))
            return
        finally:
            tmp_file.close()
            os.close(handle)
            os.remove(resaved)

        # Trick to convert images like PNG to a format comparable with JPEG.
        if im.mode != "RGB":
            im = im.convert("RGB")

        # Create ELA image.
        try:
            ela_im = ImageChops.difference(im, resaved_im)
        except Exception as e:
            logger.warning("Unable to calculate ELA difference: {0}".format(e))
            return

        # Calculate difference
        extrema = ela_im.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        if not max_diff:
            return
        scale = 255.0/max_diff
        ela_im = ImageEnhance.Brightness(ela_im).enhance(scale)
        self.results["ela"]["max_difference"] = max([ex[1] for ex in extrema])

        # Resize image if it's too big.
        width, height = ela_im.size
        if width > 1800:
            ela_im.thumbnail([1800, 1800], Image.ANTIALIAS)

        # Save image.
        try:
            img = image2str(ela_im)
            self.results["ela"]["ela_image"] = save_file(img, content_type="image/jpeg")
        except Exception as e:
            logger.warning("ELA error saving image: {0}".format(e))
        finally:
            return self.results
