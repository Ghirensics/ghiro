# Ghiro - Copyright (C) 2013-2014 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import hashlib
import tempfile
import os
import gridfs
import logging
import magic
import zlib

import analyzer.utils as utils
import analyzer.db as db

from gi.repository import GExiv2
from copy import deepcopy
from PIL import Image, ImageChops, ImageEnhance
from itertools import izip

from analyzer.signatures import SignatureRunner

logger = logging.getLogger("processor")

class MIMEAnalyzer():
    """Extracts MIME information."""

    @staticmethod
    def get_magic_filetype(file_path):
        """Get magic file type.
        @param file_path: file path
        @return: file type
        """
        mime = magic.Magic(mime=True)
        content_type = mime.from_file(file_path)
        return content_type

    @staticmethod
    def get_filetype(file_path):
        """Get extended file type.
        @param file_path: file path
        @return: file type
        """
        return magic.from_file(file_path)

class MetadataAnalyzer():
    """Extracts image metadata."""

    def __init__(self, file_path):
        try:
            self.metadata = GExiv2.Metadata(file_path)
        except Exception as e:
            logger.warning("Unable to read image metadata: {0}".format(e))
            self.metadata = None

        self.results = utils.AutoVivification()

    def _get_comment(self):
        """Extract comment."""
        if self.metadata.get_comment():
            self.results["comment"] = utils.to_unicode(self.metadata.get_comment())

    def _get_dimensions(self):
        """Extract image dimensions."""
        self.results["dimensions"] = [self.metadata.get_pixel_width(), self.metadata.get_pixel_height()]

    def _add_key(self, key, value):
        """Add a metadata key to results.
        @param key: key in full format (example: Exif.Photo.Size)
        @param value: value
        """
        family, group, tag = key.split(".")
        # Skipping keys wih empty values, they will not appear in report.
        if value and value != "" and value != "None":
            self.results[family][group][tag] = utils.to_unicode(value)
        # Add key description to database.
        utils.add_metadata_description(key, self.metadata.get_tag_description(key))

    def _get_xmp(self):
        """Extract XMP metadata."""
        for key in self.metadata.get_xmp_tags():
            self._add_key(key, self.metadata.get(key))

    def _get_iptc(self):
        """Extract IPTC metadata."""
        for key in self.metadata.get_iptc_tags():
            self._add_key(key, self.metadata.get(key))

    def _get_exif(self):
        """Extract EXIF metadata."""
        for key in self.metadata.get_exif_tags():
            self._add_key(key, self.metadata.get(key))

    def _get_previews(self):
        """Extract previews."""
        if len(self.metadata.get_preview_properties()) > 0:
            # Fetched previews key.
            self.results["preview"] = []

            for preview in self.metadata.get_preview_properties():
                p = utils.AutoVivification()
                p["mime_type"] = preview.get_mime_type()
                p["size"] = len(self.metadata.get_preview_image(preview).get_data())
                p["ext"] = preview.get_extension()
                p["dimensions"] = [preview.get_width(), preview.get_height()]

                # Resize if needed, and store.
                try:
                    img = utils.str2image(self.metadata.get_preview_image(preview).get_data())
                    if preview.get_width() > 256 or preview.get_height() > 160:
                        p["original_file"] = db.save_file(utils.image2str(img), content_type="image/jpeg")
                    img.thumbnail([256, 160], Image.ANTIALIAS)
                    p["file"] = db.save_file(utils.image2str(img), content_type="image/jpeg")
                except Exception as e:
                    logger.warning("Error reading preview: {0}".format(e))
                    continue
                finally:
                    # Save.
                    self.results["preview"].append(p)

    def _get_gps_data(self):
        """Extract GPS data."""
        if self.metadata.get_gps_info() != (0.0, 0.0, 0.0):
            self.results["gps"] = {
                # Longitude a latitude are in a separate key to be indexed in mongo spatial index.
                "pos": {"Longitude": float(self.metadata.get_gps_longitude()),
                        "Latitude": float(self.metadata.get_gps_latitude())
                        },
                "Altitude": float(self.metadata.get_gps_altitude())
            }

    def run(self):
        """Run data analysis."""
        if self.metadata:
            self._get_comment()
            self._get_dimensions()
            self._get_exif()
            self._get_iptc()
            self._get_xmp()
            self._get_previews()
            self._get_gps_data()
        return self.results

class ErrorLevelAnalyzer():
    """Error level analyzer."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.results = utils.AutoVivification()

    def run(self):
        """Run data analysis."""
        # Create temporary file.
        handle, resaved = tempfile.mkstemp()

        # Open file and resave it.
        try:
            im = Image.open(self.file_path)
            im.save(resaved, "JPEG", quality=95)
            resaved_im = Image.open(resaved)
        except IOError as e:
            logger.warning("ELA error opening image: {0}".format(e))
            return
        finally:
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
        self.results["max_difference"] = max([ex[1] for ex in extrema])

        # Resize image if it's too big.
        width, height = ela_im.size
        if width > 1800:
            ela_im.thumbnail([1800, 1800], Image.ANTIALIAS)

        # Save image.
        try:
            img = utils.image2str(ela_im)
            self.results["ela_image"] = db.save_file(img, content_type="image/jpeg")
        except Exception as e:
            logger.warning("ELA error saving image: {0}".format(e))
        finally:
            return self.results

class HashAnalyzer():
    """Hash generator."""

    def __init__(self, file_data):
        self.file_data = file_data
        self.results = utils.AutoVivification()

    def run(self):
        """Run data analysis."""
        self.results["md5"] = hashlib.md5(self.file_data).hexdigest()
        self.results['sha1'] = hashlib.sha1(self.file_data).hexdigest()
        self.results["sha224"] = hashlib.sha224(self.file_data).hexdigest()
        self.results["sha256"] = hashlib.sha256(self.file_data).hexdigest()
        self.results["sha384"] = hashlib.sha384(self.file_data).hexdigest()
        self.results["sha512"] = hashlib.sha512(self.file_data).hexdigest()
        self.results["crc32"] = "%08X".lower() % (zlib.crc32(self.file_data) & 0xFFFFFFFF,)
        return self.results

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
            i1 = utils.str2image(db.get_file(original_image_id).read())
        except IOError as e:
            logger.warning("Comparer error reading image: {0}".format(e))
            return

        # Check if thumb was resized.
        if "original_file" in preview:
            i2 = utils.str2image(db.get_file(preview["original_file"]).read())
        else:
            i2 = utils.str2image(db.get_file(preview["file"]).read())

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

class AnalyzerRunner():
    """Run image analysis."""

    def __init__(self, mongo_id, file_name=None):
        # Results storage.
        self.results = utils.AutoVivification()

        # Store image id.
        if mongo_id:
            self.orig_id = mongo_id
        else:
            raise Exception("You have to pass the original image ID")

        if file_name:
            self.file_name = file_name
        else:
            self.file_name = None

        # Read image data.
        try:
            self.file_data = db.get_file(self.orig_id).read()
        except gridfs.errors.NoFile:
            raise Exception("Image not found on GridFS storage")

        # Save a temporary file, used for analysis which needs a file on disk.
        temp_image = tempfile.NamedTemporaryFile(delete=False)
        temp_image.write(self.file_data)
        temp_image.close() # File is not immediately deleted because we used delete=False
        self.temp_image = temp_image.name

    def run(self):
        """Run analysis."""
        # Set file name.
        self.results["file_name"] = self.file_name
        self.results["file_size"] = len(self.file_data)

        # Extract MIME info.
        self.results["mime_type"] = MIMEAnalyzer.get_magic_filetype(self.temp_image)
        self.results["file_type"] = MIMEAnalyzer.get_filetype(self.temp_image)

        # Extract metadata.
        meta_anal = MetadataAnalyzer(self.temp_image)
        self.results["metadata"] = meta_anal.run()

        # ELA analysis.
        # It can be applied only on PNG and JPEG formats.
        if self.results["mime_type"] == "image/png" or self.results["mime_type"] == "image/jpeg":
            self.results["ela"] = ErrorLevelAnalyzer(self.temp_image).run()

        # Calculate hashes.
        self.results["hash"] = HashAnalyzer(self.file_data).run()

        # Compare previews to catch differences.
        if "metadata" in self.results:
            if "preview" in self.results["metadata"]:
                for preview in self.results["metadata"]["preview"]:
                    difference = ImageComparer.calculate_difference(preview, self.orig_id)
                    if difference:
                        preview["diff"], preview["diff_percent"] = difference

        # Run signatures.
        self.results["signatures"] = SignatureRunner().run(deepcopy(self.results))

        # Cleanup.
        os.remove(self.temp_image)

        return self.results