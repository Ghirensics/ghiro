# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import os
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