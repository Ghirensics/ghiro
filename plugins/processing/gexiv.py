# Ghiro - Copyright (C) 2013-2016 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import logging

from PIL import Image

from lib.db import save_file
from lib.analyzer.base import BaseProcessingModule
from lib.utils import to_unicode, AutoVivification, str2image, image2str
from analyses.models import AnalysisMetadataDescription

try:
    from gi.repository import GExiv2
    IS_GEXIV = True
except ImportError:
    IS_GEXIV = False

logger = logging.getLogger(__name__)


class GexivProcessing(BaseProcessingModule):
    """Extracts image metadata."""

    name = "Metadata Extractor (GExiv)"
    description = "This plugin performs metadata extraction using GExiv library."
    order = 10

    def check_deps(self):
        return IS_GEXIV

    def _get_comment(self):
        """Extract comment."""
        if self.metadata.get_comment():
            self.results["metadata"]["comment"] = to_unicode(self.metadata.get_comment())

    def _get_dimensions(self):
        """Extract image dimensions."""
        self.results["metadata"]["dimensions"] = [self.metadata.get_pixel_width(), self.metadata.get_pixel_height()]

    def _add_key(self, key, value):
        """Add a metadata key to results.
        @param key: key in full format (example: Exif.Photo.Size)
        @param value: value
        """
        family, group, tag = key.split(".")
        # Skipping keys wih empty values, they will not appear in report.
        if value and value != "" and value != "None":
            self.results["metadata"][family][group][tag] = to_unicode(value)
        # Add key description to database.
        AnalysisMetadataDescription.add(key, self.metadata.get_tag_description(key))

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
            self.results["metadata"]["preview"] = []

            for preview in self.metadata.get_preview_properties():
                p = AutoVivification()
                p["mime_type"] = preview.get_mime_type()
                p["size"] = preview.get_size()
                p["ext"] = preview.get_extension()
                p["dimensions"] = [preview.get_width(), preview.get_height()]

                # Resize if needed, and store.
                try:
                    img = str2image(self.metadata.get_preview_image(preview).get_data())
                    if preview.get_width() > 256 or preview.get_height() > 160:
                        p["original_file"] = save_file(image2str(img), content_type="image/jpeg")
                    img.thumbnail([256, 160], Image.ANTIALIAS)
                    p["file"] = save_file(image2str(img), content_type="image/jpeg")
                except Exception as e:
                    logger.warning("[Task {0}]: Error reading preview: {1}".format(self.task_id, e))
                    continue
                finally:
                    # Save.
                    self.results["metadata"]["preview"].append(p)

    def _get_gps_data(self):
        """Extract GPS data."""
        if self.metadata.get_gps_info() != (0.0, 0.0, 0.0):
            self.results["metadata"]["gps"] = {
                # Longitude a latitude are in a separate key to be indexed in mongo spatial index.
                "pos": {"Longitude": float(self.metadata.get_gps_longitude()),
                        "Latitude": float(self.metadata.get_gps_latitude())
                        },
                "Altitude": float(self.metadata.get_gps_altitude())
            }

    def run(self, task):
        # Save task id for logging.
        self.task_id = task.id

        # Read metadata from a temp file.
        try:
            self.metadata = GExiv2.Metadata()
            self.metadata.open_buf(bytes(task.get_file_data))
        except Exception as e:
            logger.warning("[Task {0}]: Unable to read image metadata: {1}".format(task.id, e))
            self.metadata = None

        # Run all analysis.
        if self.metadata:
            self._get_comment()
            self._get_dimensions()
            self._get_exif()
            self._get_iptc()
            self._get_xmp()
            self._get_previews()
            self._get_gps_data()

        return self.results
