# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from django.test import TestCase

from users.models import Profile
from hashes.models import List


class ListModelTest(TestCase):
    def setUp(self):
        self.user = Profile.objects.create_user(username="test", email="a@a.cp,", password="Test")
        self.user2 = Profile.objects.create_user(username="test2", email="b@a.cp,", password="Test")

    def test_is_owner(self):
        hash = List.objects.create(name="aaa", owner=self.user)
        self.assertTrue(hash.is_owner(self.user))
        self.assertFalse(hash.is_owner(self.user2))

    def test_can_read(self):
        """Owner and superuser have to read the list."""
        hash = List.objects.create(name="aaa", owner=self.user)
        # Owner.
        self.assertTrue(hash.can_read(self.user))
        # Others.
        self.assertFalse(hash.can_read(self.user2))
        # Superuser.
        superuser = Profile.objects.create_superuser(username="test3", email="a@a.cp,", password="Test")
        self.assertTrue(hash.can_read(superuser))

    def test_can_read_public(self):
        """All have to read the list."""
        hash = List.objects.create(name="aaa", owner=self.user, public=True)
        # Owner.
        self.assertTrue(hash.can_read(self.user))
        # Others.
        self.assertTrue(hash.can_read(self.user2))
        # Superuser.
        superuser = Profile.objects.create_superuser(username="test3", email="a@a.cp,", password="Test")
        self.assertTrue(hash.can_read(superuser))

    def test_can_write(self):
        """Owner and superuser have to write the list."""
        hash = List.objects.create(name="aaa", owner=self.user)
        # Owner.
        self.assertTrue(hash.can_write(self.user))
        # Others.
        self.assertFalse(hash.can_write(self.user2))
        # Superuser.
        superuser = Profile.objects.create_superuser(username="test3", email="a@a.cp,", password="Test")
        self.assertTrue(hash.can_write(superuser))
