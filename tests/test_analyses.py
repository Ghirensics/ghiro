# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

import os
import tempfile
import shutil

from django.test import TestCase
from django.conf import settings

from users.models import Profile
from analyses.models import Case, Analysis
from analyses.management.commands.auto_upload import Command


class CaseModelTest(TestCase):
    def setUp(self):
        self.user = Profile.objects.create_user(username="test", email="a@a.cp,", password="Test")
        self.user2 = Profile.objects.create_user(username="test2", email="b@a.cp,", password="Test")

    def test_is_owner(self):
        case = Case.objects.create(name="aaa", owner=self.user)
        self.assertTrue(case.is_owner(self.user))
        self.assertFalse(case.is_owner(self.user2))

    def test_is_in_users(self):
        case = Case.objects.create(name="aaa", owner=self.user)
        case.users.add(self.user)
        self.assertTrue(case.is_in_users(self.user))
        self.assertFalse(case.is_in_users(self.user2))

    def test_can_read(self):
        """Owner, users in user list and superuser have to read the analysis."""
        case = Case.objects.create(name="aaa", owner=self.user)
        case.users.add(self.user2)
        # User.
        self.assertTrue(case.can_read(self.user))
        # User in list.
        self.assertTrue(case.can_read(self.user2))
        # Superuser.
        superuser = Profile.objects.create_superuser(username="test3", email="a@a.cp,", password="Test")
        self.assertTrue(case.can_read(superuser))
        # Fail.
        bad_user = Profile.objects.create_user(username="test4", email="a@a.cp,", password="Test")
        self.assertFalse(case.can_read(bad_user))

    def test_can_write(self):
        """Owner, users in user list and superuser have to write the analysis."""
        case = Case.objects.create(name="aaa", owner=self.user)
        case.users.add(self.user2)
        # User.
        self.assertTrue(case.can_write(self.user))
        # User in list.
        self.assertTrue(case.can_write(self.user2))
        # Superuser.
        superuser = Profile.objects.create_superuser(username="test3", email="a@a.cp,", password="Test")
        self.assertTrue(case.can_write(superuser))
        # Fail.
        bad_user = Profile.objects.create_user(username="test4", email="a@a.cp,", password="Test")
        self.assertFalse(case.can_write(bad_user))

    def test_stripping_attrs(self):
        """Strip spaces in some attributes."""
        case = Case.objects.create(name=" a ", description=" a ", owner=self.user)
        self.assertEqual(case.name, "a")
        self.assertEqual(case.description, "a")

    def test_set_updated_at(self):
        """Updated_at should be automatically updated at save()."""
        case = Case.objects.create(name="a", owner=self.user)
        t1 = case.updated_at
        # Save again, updated_at should be updated.
        case.save()
        self.assertNotEqual(t1, case.updated_at)

    def test_directory_name(self):
        """Test directory name syntax."""
        case = Case.objects.create(name="a", owner=self.user, id=42)
        self.assertEqual(case.directory_name, "Case_id_%s" % case.id)

    def test_auto_upload_sync_creation(self):
        """Tests automated case folder creation."""
        # Create temporary directory to store everything.
        tmp_path = tempfile.mkdtemp()
        # Build the ghiro path for auto upload.
        ghiro_path = os.path.join(tmp_path, "ghiro-test")
        # Set path and test.
        settings.AUTO_UPLOAD_DIR = ghiro_path
        # Create base dir.
        Command.create_auto_upload_dirs()
        # Create case.
        case = Case.objects.create(name="a", owner=self.user)
        dir_name = os.path.join(settings.AUTO_UPLOAD_DIR, case.directory_name)
        self.assertTrue(os.path.exists(dir_name))
        # Cleanup.
        shutil.rmtree(tmp_path)

class AnalysisModelTest(TestCase):
    def setUp(self):
        self.user = Profile.objects.create_user(username="test", email="a@a.cp,", password="Test")
        self.user2 = Profile.objects.create_user(username="test2", email="b@a.cp,", password="Test")

    def test_is_owner(self):
        anal = Analysis.objects.create(owner=self.user)
        self.assertTrue(anal.is_owner(self.user))
        self.assertFalse(anal.is_owner(self.user2))

    def test_can_read(self):
        """Owner and superuser have to read the analysis."""
        anal = Analysis.objects.create(owner=self.user)
        # User.
        self.assertTrue(anal.can_read(self.user))
        # Superuser.
        superuser = Profile.objects.create_superuser(username="test3", email="a@a.cp,", password="Test")
        self.assertTrue(anal.can_read(superuser))
        # Fail.
        self.assertFalse(anal.can_read(self.user2))

    def test_can_write(self):
        """Owner and superuser have to write the analysis."""
        anal = Analysis.objects.create(owner=self.user)
        # User.
        self.assertTrue(anal.can_write(self.user))
        # Superuser.
        superuser = Profile.objects.create_superuser(username="test3", email="a@a.cp,", password="Test")
        self.assertTrue(anal.can_write(superuser))
        # Fail.
        self.assertFalse(anal.can_write(self.user2))