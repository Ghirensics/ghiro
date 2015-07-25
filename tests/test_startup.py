# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import os
import shutil
import tempfile
from django.test import TestCase
from django.conf import settings

from lib.startup import create_auto_upload_dirs
from analyses.models import Case
from users.models import Profile


class CreateAutoUploadDirTest(TestCase):
    def setUp(self):
        self.user = Profile.objects.create_user(username="test", email="a@a.cp,", password="Test")

    def test_missing_auto_upload_dir(self):
        """Test for AUTO_UPLOAD_DIR missing. It should exit returning False."""
        # None case.
        settings.AUTO_UPLOAD_DIR = None
        self.assertFalse(create_auto_upload_dirs())
        # Empty case.
        settings.AUTO_UPLOAD_DIR = ""
        self.assertFalse(create_auto_upload_dirs())

    def test_create_auto_upload_dir(self):
        """Test for AUTO_UPLOAD_DIR creation when missing."""
        # Create temporary directory to store everything.
        tmp_path = tempfile.mkdtemp()
        # Build the ghiro path for auto upload.
        ghiro_path = os.path.join(tmp_path, "ghiro-test")
        # Set path and test.
        settings.AUTO_UPLOAD_DIR = ghiro_path
        self.assertNotEqual(create_auto_upload_dirs(), False)
        self.assertTrue(os.path.exists(ghiro_path))
        # Cleanup.
        shutil.rmtree(tmp_path)

    def test_case_folders_creation(self):
        # Create cases.
        case1 = Case.objects.create(name="aaa", owner=self.user)
        case2 = Case.objects.create(name="aab", owner=self.user)
        # Create temporary directory to store everything.
        tmp_path = tempfile.mkdtemp()
        # Build the ghiro path for auto upload.
        ghiro_path = os.path.join(tmp_path, "ghiro-test")
        # Set path and create folders.
        settings.AUTO_UPLOAD_DIR = ghiro_path
        create_auto_upload_dirs()
        # Test.
        for case in [case1, case2]:
            case_path = os.path.join(ghiro_path, "Case_id_%s" % case.id)
            self.assertTrue(os.path.exists(case_path))
        # Cleanup.
        shutil.rmtree(tmp_path)

    def test_cleanup_auto_upload_dir(self):
        """Test for AUTO_UPLOAD_STARTUP_CLEANUP."""
        # Create temporary directory to store everything.
        tmp_path = tempfile.mkdtemp()
        # Build the ghiro path for auto upload.
        ghiro_path = os.path.join(tmp_path, "ghiro-test")
        # Set path and create folders.
        settings.AUTO_UPLOAD_DIR = ghiro_path
        os.mkdir(ghiro_path)
        # Test folder.
        test_path = os.path.join(ghiro_path, "test")
        os.mkdir(test_path)
        # Test 1: not cleaning.
        settings.AUTO_UPLOAD_STARTUP_CLEANUP = False
        create_auto_upload_dirs()
        self.assertTrue(os.path.exists(test_path))
        # Test 2: cleaning.
        settings.AUTO_UPLOAD_STARTUP_CLEANUP = True
        create_auto_upload_dirs()
        self.assertFalse(os.path.exists(test_path))
        # Cleanup.
        shutil.rmtree(tmp_path)