# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from django.test import TestCase
from django.conf import settings

from lib.analyzer.processing import AnalysisManager


class AnalysisManagerTest(TestCase):
    def setUp(self):
        self.am = AnalysisManager()

    def test_parallelism_positive(self):
        """Parallelism should be always greater than 0."""
        self.assertGreater(self.am.get_parallelism(), 0)

    def test_parallelism_sqlite(self):
        """Parallelism should be always greater than 0."""
        settings.DATABASES["default"]["ENGINE"] = "sqlite3"
        self.assertEqual(self.am.get_parallelism(), 1)

    def tearDown(self):
         self.am.stop()