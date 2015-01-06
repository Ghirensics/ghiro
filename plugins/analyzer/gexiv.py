# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import logging

from PIL import Image

from lib.db import save_file
from lib.analyzer.base import BaseAnalyzerModule
from lib.utils import str2temp_file, to_unicode, add_metadata_description, AutoVivification, str2image, image2str

try:
    from gi.repository import GExiv2
    IS_GEXIV = True
except ImportError:
    IS_GEXIV = False

logger = logging.getLogger(__name__)


class GexivAnalyzer(BaseAnalyzerModule):
    """Extracts image metadata."""

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
        add_metadata_description(key, self.metadata.get_tag_description(key))

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
                p["size"] = len(self.metadata.get_preview_image(preview).get_data())
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
                    logger.warning("Error reading preview: {0}".format(e))
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
        # Read metadata from a temp file.
        try:
            tmp_file = str2temp_file(task.get_file_data)
            self.metadata = GExiv2.Metadata()
            self.metadata.open_path(str(tmp_file.name))
        except Exception as e:
            logger.warning("Unable to read image metadata: {0}".format(e))
            self.metadata = None
        finally:
            tmp_file.close()

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
