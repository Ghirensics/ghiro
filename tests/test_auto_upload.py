# Ghiro - Copyright (C) 2013-2016 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import os
import tempfile
import shutil
from django.test import TestCase
from django.conf import settings

from analyses.management.commands.auto_upload import Command
from analyses.models import Case, Analysis
from users.models import Profile


class CreateAutoUploadDirTest(TestCase):
    def setUp(self):
        self.user = Profile.objects.create_user(username="test", email="a@a.cp,", password="Test")

    def test_missing_auto_upload_dir(self):
        """Test for AUTO_UPLOAD_DIR missing. It should exit returning False."""
        # None case.
        settings.AUTO_UPLOAD_DIR = None
        self.assertFalse(Command.create_auto_upload_dirs())
        # Empty case.
        settings.AUTO_UPLOAD_DIR = ""
        self.assertFalse(Command.create_auto_upload_dirs())

    def test_create_auto_upload_dir(self):
        """Test for AUTO_UPLOAD_DIR creation when missing."""
        # Create temporary directory to store everything.
        tmp_path = tempfile.mkdtemp()
        # Build the ghiro path for auto upload.
        ghiro_path = os.path.join(tmp_path, "ghiro-test")
        # Set path and test.
        settings.AUTO_UPLOAD_DIR = ghiro_path
        self.assertNotEqual(Command.create_auto_upload_dirs(), False)
        self.assertTrue(os.path.exists(ghiro_path))
        # Cleanup.
        shutil.rmtree(tmp_path)

    def test_existent_auto_upload_dir(self):
        """Test for AUTO_UPLOAD_DIR creation when it already exist."""
        # Create cases.
        case1 = Case.objects.create(name="aaa", owner=self.user)
        case2 = Case.objects.create(name="aab", owner=self.user)
        # Create temporary directory to store everything.
        tmp_path = tempfile.mkdtemp()
        # Build the ghiro path for auto upload.
        ghiro_path = os.path.join(tmp_path, "ghiro-test")
        # Create AUTO_UPLOAD_DIR.
        os.mkdir(ghiro_path)
        # Set path and test.
        settings.AUTO_UPLOAD_DIR = ghiro_path
        self.assertNotEqual(Command.create_auto_upload_dirs(), False)
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
        Command.create_auto_upload_dirs()
        # Test.
        for case in [case1, case2]:
            case_path = os.path.join(ghiro_path, case.directory_name)
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
        Command.create_auto_upload_dirs()
        self.assertTrue(os.path.exists(test_path))
        # Test 2: cleaning.
        settings.AUTO_UPLOAD_STARTUP_CLEANUP = True
        Command.create_auto_upload_dirs()
        self.assertFalse(os.path.exists(test_path))
        # Cleanup.
        shutil.rmtree(tmp_path)

class ParseDirNameTest(TestCase):
    """Tests parse_dir_name()."""

    def setUp(self):
        self.c = Command()
        self.user = Profile.objects.create_user(username="test", email="a@a.cp,", password="Test")

    def test_parse_dir_name_one_digit(self):
        """Tests parsing of directory name, expected cases: one digit."""
        case = Case.objects.create(name="aaa", owner=self.user, id=4)
        self.assertEqual(self.c.parse_dir_name(case.directory_name), case)

    def test_parse_dir_name_absolute_path(self):
        """Tests parsing of directory name, expected cases: absolute path."""
        case = Case.objects.create(name="aaa", owner=self.user, id=4)
        dir_name = os.path.join("/tmp/ghiro", case.directory_name)
        self.assertEqual(self.c.parse_dir_name(dir_name), case)

    def test_parse_dir_name_many_digits(self):
        """Tests parsing of directory name, expected cases: many digits."""
        case = Case.objects.create(name="aaa", owner=self.user, id=42)
        self.assertEqual(self.c.parse_dir_name(case.directory_name), case)

    def test_parse_dir_name_bad_format(self):
        """Tests parsing of directory name, unexpected cases: literal."""
        dir_name = "Case_id_aA"
        self.assertEqual(self.c.parse_dir_name(dir_name), None)

class SubmitFileTest(TestCase):
    """Tests submit_file()."""

    def setUp(self):
        self.c = Command()
        self.user = Profile.objects.create_user(username="test", email="a@a.cp,", password="Test")
        test_image = os.path.join("tests", "fixtures", "images", "1x1.png")
        test_path = tempfile.mkdtemp()
        shutil.copy(test_image, test_path)
        self.image_path = os.path.join(test_path, "1x1.png")
        self.case = Case.objects.create(name="aaa", owner=self.user)

    def test_submit_file_no_remove(self):
        """Tests file submission, don't remove original file"""
        # Test analysis added.
        settings.AUTO_UPLOAD_DEL_ORIGINAL = False
        t1 = Analysis.objects.count()
        self.c.submit_file(self.image_path, self.case)
        self.assertNotEqual(t1, Analysis.objects.count())
        # Test no remove.
        self.assertTrue(os.path.exists(self.image_path))

    def test_submit_file_with_remove(self):
        """Tests file submission, remove original file"""
        # Test analysis added.
        settings.AUTO_UPLOAD_DEL_ORIGINAL = True
        t1 = Analysis.objects.count()
        self.c.submit_file(self.image_path, self.case)
        self.assertNotEqual(t1, Analysis.objects.count())
        # Test no remove.
        self.assertFalse(os.path.exists(self.image_path))