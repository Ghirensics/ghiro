# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import os
from PIL import Image
from django.test import TestCase

from lib.utils import *


class ImportIsAvailableTest(TestCase):

    def test_can_import(self):
        self.assertTrue(import_is_available("os"))

    def test_cannot_import(self):
        self.assertFalse(import_is_available("antanitapioco"))

class GetContentTypeFromFileTest(TestCase):

    def setUp(self):
        self.image = os.path.join("tests", "fixtures", "images", "1x1.png")

    def test_content_type(self):
        self.assertEqual(get_content_type_from_file(self.image), "image/png")

class Image2StrTest(TestCase):
    """Tests image2str()."""

    def setUp(self):
        self.image = Image.new("RGB", (10, 50))

    def test_convert_to_str(self):
        """Tests the returned data type, should be string."""
        # TODO: this test should be better fixed to meet both py2 and py3 strings.
        self.assertTrue(isinstance(image2str(self.image), str) or isinstance(image2str(self.image), bytes))